import cgi # CGIモジュールのインポート
import cgitb
import sys
import requests
import json

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello ITA_API_TEST_APP !!')

def form(request):
    return render(request, 'form.html')

def editRestApi(request):

#    cgitb.enable() # デバッグに使うので、本番環境では記述しない

    replicas = request.POST["Replicas"]
    image = request.POST["Image"]
#    form = cgi.FieldStorage() # フォームデータを取得する

    httpRet = ""
    httpRet += "Content-Type: text/html; charset=UTF-8" # HTMLを記述するためのヘッダ
    httpRet += ""

    # フォームのデータが入力されていない場合
 #   if "Replicas" not in form:
    if not replicas:
        httpRet += "<h1>Error!</h1>"
        httpRet += "<br>"
        httpRet += "Replicasを入力してください！"
        httpRet += "<a href='/ita_api_test/form'><button type='submit'>戻る</button></a>"
        return HttpResponse(httpRet)

#    if "Image" not in form:
    if not image:
        httpRet += "<h1>Error!</h1>"
        httpRet += "<br>"
        httpRet += "Imageを入力してください！"
        httpRet += "<a href='/ita_api_test/form'><button type='submit'>戻る</button></a>"
        return HttpResponse(httpRet)

    # # データの値を取得する
    # replicas = form.getvalue("Replicas")
    # image = form.getvalue("Image")

    httpRet += "Replicas:" + replicas + "<br />"
    httpRet += "Image:" + image + "<br />"

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

    httpRet += "オペレーション:" + str(d['resultdata']['CONTENTS']['BODY'][1][9]) + "<br />"

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
        "9":"" + str(d['resultdata']['CONTENTS']['BODY'][1][9]) + "", \
        "10":"" + replicas + "", \
        "11":"" + image + "", \
        "12":"20210106_1405",  \
        "14":"2020/01/06 13:00:00", \
        "15": "" + timestamp + "" , \
        "16":"管理者" }]

    # json文字列に変換（"utf-8"形式に自動エンコードされる）
    json_data = json.dumps(str_data)

    # リクエスト送信
    edit_response = requests.post('http://it-automation-default.apps.ky-labo-ops2.exastro-ops-2.com/default/menu/07_rest_api_ver1.php?no=0000000013', headers=edit_headers, data=json_data)

    httpRet += str(json.loads(edit_response.text))

    return HttpResponse(httpRet + '<br /><br />Update Complete !!')

