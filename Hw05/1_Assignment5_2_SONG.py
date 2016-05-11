# -*- coding:utf-8 -*-
## スクリプトの文字コードを指定(Python 2.xでは必須らしい)

##############################################################
## ファイル名：Hw05-SONG.py
##
## 説明: 韓国の第19代国会議員総選挙の自治体別の投票率を時系列で収集
##      そのために中央選挙管理委員会の選挙統計システムを利用する。
## 出力: Hw05-SONG.csv
## 提出者: 宋ジェヒョン (123J009J)
## 作成日: 2014年11月1日
##############################################################

## 中央選挙管理委員会→選挙統計システム→第19代国会議員選挙→投・開票→投票進行のURLをpathへ書き込む
## 広域自治体のコードであるcityCodeは空白({})に
path = 'http://info.nec.go.kr/electioninfo/electionInfo_report.action?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fvc%2Fvcvp01.jsp&topMenuId=VC&secondMenuId=VCVP&menuId=VCVP01&statementId=VCVP01_%232&sggTime=20%EC%8B%9C&cityCode={}&timeCode=0&x=26&y=5'

##　広域自治体のコードをlist型に
pages = ["1100", "2600", "2700", # ソウル、釜山、大邸
         "2800", "2900", "3000", # 仁川、光州、大田
         "3100", "5100", "4100", # 蔚山、世宗、京義
         "4200", "4300", "4400", # 江原、忠北、忠南
         "4500", "4600", "4700", # 全北、全南、慶北
         "4800", "4900"]         # 慶南、済州

## 広域自治体の名前(略称)
region = ["Seoul", "Busan", "Daegu", 
          "Incheon", "Gwangju", "Daejeon", 
          "Ulsan", "Sejong", "Gyeonggi", 
          "Gangwon", "Choong-buk", "Choong-nam", 
          "Jeong-buk", "Jeong-nam", "Gyeong-buk", 
          "Gyeong-nam", "Jeju"]
## (今思いついたが、Dictionary型でもいいかも)

## テーブルの列は共通的に13
widths = 13

## URL openerを用意する
import urllib2
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozila/5.0')]

## csvとして書き込むためにcsvライブラリを呼び出す
import csv
filename = 'Hw05_Prob2-SONG.csv'
writecsv = csv.writer(file(filename, 'w'))

## 第１行を書き込む(変数名)
## cf)元々は基礎自治体に含まれない行政区(日本の政令指定都市の
##    区に相当)もここでは含まれる。ソウル特別市と６広域市の下
##    位行政区域である自治区も基礎自治体であるため含まれる。
writecsv.writerow([
    'Region',                   # 広域自治体名
    'Municipality',             # 基礎自治体名(ハングル)
    '# of electorate',          # 選挙人数
    '07:00', '09:00', '11:00',  # 午前 7, 9, 11時
    '12:00', '13:00', '14:00',  # 午後 12, 1, 2時
    '15:00', '16:00', '17:00',  # 午後 3, 4, 5時
    '18:00', '# of voters'])    # 午後 6時, 投票者数


## 正規表現を用いるためにreライブラリを呼び出す
import re
## タグ除去のための正規表現
reg_exp1 = re.compile(r'<.*?>')
## 括弧と括弧内の内容を除去するための正規表現
reg_exp2 = re.compile(r'\(.*?\)')

## スクラッピングのためにBeautifulSoupライブラリを呼び出し,
## BSという略称を指定
from bs4 import BeautifulSoup as BS

## カウンター初期化
counter = 0
for page in pages:       ## ページ数だけループ
    try:
        ## pathで指定したURLとpagesで指定した広域自治体コード
        ## を合わせたURLをURL openerでアクセスし、
        ## BeautifulSoupライブラリでスクラッピング
        soup = BS(opener.open(path.format(page)))

        ## テーブルのセルを意味する<td>タグを検索し、
        ## オブジェクト, resへストック (list型)
        res = soup.findAll('td')

        ## 最初の行(合計)を削除する。
        ## 13列のテーブルであるため[0~12]の要素は使わない
        res = res[13:]

        ## 広域自治体名をregに
        reg = region[counter]

        ## リスト型であるresを列数(13)で割り、行数を計算
        num = len(res) / 13

        for i in range (0, num): 
            ## 基礎自治体名が書いてあるセルを抽出
            muni = res[0+13*i]
            ## reg_exp1でタグを除去し、空白も除去
            muni = reg_exp1.sub('', str(muni))
            muni = muni.strip()
                
            ## 選挙人数のセルを抽出
            electo = res[1+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            electo = reg_exp1.sub('', str(electo))
            electo = reg_exp2.sub('', str(electo))
            electo = int(electo.replace(',', ''))
            
            ## 午前7時の投票者数のセルを抽出
            t7 = res[2+13*i]
            ## タグ、千単位のカンマ区切りを除去
            t7 = reg_exp1.sub('', str(t7))
            t7 = int(t7.replace(',', ''))

            ## 午前9時の投票者数のセルを抽出
            t9 = res[3+13*i]
            ## タグ、千単位のカンマ区切りを除去
            t9 = reg_exp1.sub('', str(t9))
            t9 = int(t9.replace(',', ''))

            ## 午前11時の投票者数のセルを抽出
            t11 = res[4+13*i]
            ## タグ、千単位のカンマ区切りを除去
            t11 = reg_exp1.sub('', str(t11))
            t11 = int(t11.replace(',', ''))

            ## 午後12時の投票者数のセルを抽出
            t12 = res[5+13*i]
            ## タグ、千単位のカンマ区切りを除去
            t12 = reg_exp1.sub('', str(t12))
            t12 = int(t12.replace(',', ''))

            ## 午後1時の投票者数のセルを抽出
            t13 = res[6+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            ## (午後1時から不在者投票も含まれる)
            t13 = reg_exp1.sub('', str(t13))
            t13 = reg_exp2.sub('', str(t13))
            t13 = int(t13.replace(',', ''))

            ## 午後2時の投票者数のセルを抽出
            t14 = res[7+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            t14 = reg_exp1.sub('', str(t14))
            t14 = reg_exp2.sub('', str(t14))
            t14 = int(t14.replace(',', ''))

            ## 午後3時の投票者数のセルを抽出
            t15 = res[8+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            t15 = reg_exp1.sub('', str(t15))
            t15 = reg_exp2.sub('', str(t15))
            t15 = int(t15.replace(',', ''))

            ## 午後4時の投票者数のセルを抽出
            t16 = res[9+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            t16 = reg_exp1.sub('', str(t16))
            t16 = reg_exp2.sub('', str(t16))
            t16 = int(t16.replace(',', ''))

            ## 午後5時の投票者数のセルを抽出
            t17 = res[10+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            t17 = reg_exp1.sub('', str(t17))
            t17 = reg_exp2.sub('', str(t17))
            t17 = int(t17.replace(',', ''))

            ## 午後6時の投票者数のセルを抽出
            t18 = res[11+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            t18 = reg_exp1.sub('', str(t18))
            t18 = reg_exp2.sub('', str(t18))
            t18 = int(t18.replace(',', ''))

            ## 投票者数のセルを抽出
            voter = res[12+13*i]
            ## タグ、括弧、千単位のカンマ区切りを除去
            voter = reg_exp1.sub('', str(t18))
            voter = reg_exp2.sub('', str(t18))
            voter = int(voter.replace(',', ''))

            ## 以上のオブジェクトをcsvファイルに書き込む
            writecsv.writerow([
                reg, muni, electo,
                t7, t9, t11, t12,
                t13, t14, t15, t16,
                t17, t18, voter
                ])
   
    ## 例外を指定し、エラーメッセージを出力
    except urllib2.HTTPError as instance:
        if instance.code == 404:
            ## ページが見つからないとエラーメッセージ
            print("ページが見つかりません: " + path.format(page))
        else:
            ## アクセスが拒否されるとエラーメッセージ
            print("アクセスが拒否されました: " + path.format(page))

    counter += 1 # カウンターを+1

## Show the message when scraping finishes
print("スクラッピングを完了しました。")

##=========================================================
## まとめ：実際のホームページと結果を比べたら正確にスクラッピング
## 　　　　できたことが分かる。ただ、17ページならわざわざPython
## 　　　　使わず、OutWit Hubでもいいと思う。
## 　　　　ただ、得票数は投票所ごとのデータも載っているため、その
## 　　　　時には非常に役に立つと思う。(テーブルの形がややこしいが)
##=========================================================