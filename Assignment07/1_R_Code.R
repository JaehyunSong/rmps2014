dataset <- read.csv("dataset.csv")
head(dataset)

c.win <- dataset$win - 2
c.age <- dataset$age - 55

model1 <- lm(rows ~ popcom + unpopcom + c.win + sex + c.age + pr + region, data=dataset)
model2 <- lm(rows ~ popcom + unpopcom + c.win + sex + c.age + pr + region + c.win * popcom + c.win * unpopcom, data=dataset)
summary(model1)
summary(model2)

require(ggplot2)
theme_set(theme_gray(base_size=12, base_family="HiraKakuProN-W3"))

model1.df <- data.frame(row.no = c(7:1),
                        variable = c("人気委員会", "忌避委員会", "当選回数", "女性", 
                                     "年齢", "比例ダミー", "地域ダミー"),
                        coef = coef(model1)[-1],
                        lower.se = confint(model1)[-1, 1],
                        upper.se = confint(model1)[-1, 2])

row.names(model1.df) <- NULL

model1.plot <- ggplot(data = model1.df, aes(x = reorder(variable, row.no), y = coef, 
                                            ymin = lower.se,
                                            ymax = upper.se)) +
  geom_pointrange(size = 1.4) +
  geom_hline(aes(intercept = 0), linetype = "dotted") +
  xlab("説明変数") + ylab("係数の推定値") +
  theme(text = element_text(size=20)) +
  coord_flip()

print(model1.plot)

model2.df <- data.frame(row.no = c(9:1),
                        variable = c("人気委員会", "忌避委員会", "当選回数", "女性", 
                                     "年齢", "比例ダミー", "地域ダミー",
                                     "人気×当選", "忌避×当選"),
                        coef = coef(model2)[-1],
                        lower.se = confint(model2)[-1, 1],
                        upper.se = confint(model2)[-1, 2])

row.names(model2.df) <- NULL

model2.plot <- ggplot(data = model2.df, aes(x = reorder(variable, row.no), y = coef, 
                                            ymin = lower.se,
                                            ymax = upper.se)) +
  geom_pointrange(size = 1.4) +
  geom_hline(aes(intercept = 0), linetype = "dotted") +
  xlab("説明変数") + ylab("係数の推定値") +
  theme(text = element_text(size=20)) +
  coord_flip()

print(model2.plot)

sim1 <- read.csv("simulation1.csv")
sim2 <- read.csv("simulation2.csv")

sim1_result <- as.matrix(sim1) %*% matrix(coef(model2), ncol=1)
sim2_result <- as.matrix(sim2) %*% matrix(coef(model2), ncol=1)

sim_result <- data.frame(win=c(1:6), unpop=sim1_result, nounpop=sim2_result)
sim_result

sim.result2 <- ggplot(data = sim_result, aes(x = win)) + 
  geom_line(aes(y = unpop, color = "red")) + 
  geom_line(aes(y = nounpop, color = "blue")) +
  labs(x = "当選回数", y = "座席の列") +
  scale_color_discrete(name = "人気委員会",
                       labels = c("未所属", "所属")) +
  scale_x_continuous(breaks = 1:6) + 
  scale_y_continuous(breaks = 1:10) +
  theme(text = element_text(size=20))

print(sim.result2)

sim.win <- seq(-1, 4, by = 0.1)
int <- model2$coef[2] + model2$coef[9] * sim.win

se_int <- sqrt(vcov(model2)[2, 2] + (sim.win^2) * vcov(model2)[9, 9] + 2 * sim.win * vcov(model2)[2, 9])

int_ll <- int - 1.98 * se_int
int_ul <- int + 1.98 * se_int

final.data <- data.frame(win = seq(1, 6, by = 0.1), me = int, ul = int_ul, ll = int_ll)
head(final.data)

me.plot1 <- ggplot(data = final.data, aes(x = win)) + 
  geom_line(aes(y = me)) + 
  geom_line(aes(y = ul), linetype = "dashed") +
  geom_line(aes(y = ll), linetype = "dashed") +
  labs(x = "当選回数", y = "人気委員会所属の限界効果") +
  scale_x_continuous(breaks = 1:6) + 
  scale_y_continuous(breaks = -3:3) +
  geom_hline(yintercept = 0) +
  theme(text = element_text(size=20), legend.position="none")

print(me.plot1)

sim.win <- seq(-1, 4, by = 0.1)
int <- model2$coef[3] + model2$coef[10] * sim.win

se_int <- sqrt(vcov(model2)[3, 3] + (sim.win^2) * vcov(model2)[10, 10] + 2 * sim.win * vcov(model2)[3, 10])

int_ll <- int - 1.98 * se_int
int_ul <- int + 1.98 * se_int

final.data <- data.frame(win = seq(1, 6, by = 0.1), me = int, ul = int_ul, ll = int_ll)
head(final.data)

me.plot2 <- ggplot(data = final.data, aes(x = win)) + 
  geom_line(aes(y = me)) + 
  geom_line(aes(y = ul), linetype = "dashed") +
  geom_line(aes(y = ll), linetype = "dashed") +
  labs(x = "当選回数", y = "忌避委員会所属の限界効果") +
  scale_x_continuous(breaks = 1:6) + 
  scale_y_continuous(breaks = -10:1) +
  geom_hline(yintercept = 0) +
  theme(text = element_text(size=20), legend.position="none")

print(me.plot2)