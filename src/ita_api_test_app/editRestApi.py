import cgi # CGIモジュールのインポート
import cgitb
import sys
import requests
import json

cgitb.enable() # デバッグに使うので、本番環境では記述しない

form = cgi.FieldStorage() # フォームデータを取得する

print("Content-Type: text/html; charset=UTF-8") # HTMLを記述するためのヘッダ
print("")

# フォームのデータが入力されていない場合
if "Replicas" not in form:
    print("<h1>Error!</h1>")
    print("<br>")
    print("Replicasを入力してください！")
    print("<a href='/CICDUpdate.html'><button type='submit'>戻る</button></a>")
    sys.exit()

if "Image" not in form:
    print("<h1>Error!</h1>")
    print("<br>")
    print("Imageを入力してください！")
    print("<a href='/CICDUpdate.html'><button type='submit'>戻る</button></a>")
    sys.exit()

# データの値を取得する
replicas = form.getvalue("Replicas")
image = form.getvalue("Image")

print("Replicas:" + replicas)
print("Image:" + image)

# FILTERコマンドでPOST送信する
# ヘッダ情報
filter_headers = {
    'host': 'it-automation-default.apps.ky-labo-ops2.exastro-ops-2.com:80',
    'Content-Type': 'application/json',
    'Authorization': 'YWRtaW5pc3RyYXRvcjp5KCs2ZSxTMylt',
    'X-Command': 'FILTER',
}

# リクエスト送信
filter_response = requests.post('http://it-automation-default.apps.ky-labo-ops2.exastro-ops-2.com/default/menu/07_rest_api_ver1.php?no=0000000013', headers=filter_headers)

# レスポンスのJSON文字列を辞書に変換
d = json.loads(filter_response.text)

# 更新対象の行データ(1行目)と、列データ取得（15列目：タイムスタンプ）を取得
timestamp = str(d['resultdata']['CONTENTS']['BODY'][1][15])

# EDITコマンドでPOST送信する
# ヘッダ情報
edit_headers = {
    'host': 'it-automation-default.apps.ky-labo-ops2.exastro-ops-2.com:80',
    'Content-Type': 'application/json',
    'Authorization': 'YWRtaW5pc3RyYXRvcjp5KCs2ZSxTMylt',
    'X-Command': 'EDIT',
}

# 更新パラメータを設定
str_data = [{ "0":"更新", \
    "1":"", \
    "2":"1", \
    "3":"ky-labo-ops-mente", \
    "5":"デモ用マニュフェスト配置", \
    "9":"2020\/12\/16 09:30_4:デモ用マニュフェスト配置", \
    "10":"" + Replicas + "", \
    "11":"" + Image + "", \
    "12":"20210106_1405",  \
    "14":"2020/01/06 13:00:00", \
    "15": "" + timestamp + "" , \
    "16":"管理者" }]

# json文字列に変換（"utf-8"形式に自動エンコードされる）
json_data = json.dumps(str_data)

# リクエスト送信
edit_response = requests.post('http://it-automation-default.apps.ky-labo-ops2.exastro-ops-2.com/default/menu/07_rest_api_ver1.php?no=0000000013', headers=edit_headers, data=json_data)

print(json.loads(edit_response.text))