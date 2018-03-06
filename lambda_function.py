#-*- coding:utf-8 -*-
from urlparse import urljoin
from urllib import urlencode
import urllib2 as urlrequest
import json
import random
import datetime

# CUSTOM SEARCH API周りの設定
CUSTOM_SEARCH_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CUSTOM_ENGINE_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
URL_TEMPLATE = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&searchType=image&q={search_word}"

# SLACK周りの設定
SLACK_POST_URL = "https://hooks.slack.com/services/T4YNVF84V/B98S3UKQU/XXXXXXXXXXXXXXXXXXXXXXXX"

def post_image_to_slack(search_word):
    """
    google custom serachでimageのURLを取得し，ランダムでSLACKに投稿する
    """
    # urlを複数取得する
    urls = get_image_urls(search_word)

    # urlが取得できなかった場合は投稿しない
    if len(urls) == 0:
        return "no images were found."

    # urlをランダムに選択する。（公式画像であればもう一度選択する）
    while True :
        url = random.choice(urls)
        if "img.nogizaka46.com" in url:
            # もう一度選択する
            print(url)
        else:
            break

    # slack用のメッセージを作成
    # 取得した時間によって出すメッセージを変更する
    hour = datetime.datetime.now().hour
    txt = ""
    if hour == 1:
        txt = "おはよう！今日も頑張ろう！！\n"
    elif hour == 10:
        txt = "今日もお疲れ様！19時だよ！！\n"
    post_msg = build_message(url, txt)

    # slackに投稿
    return post(post_msg)

def get_image_urls(search_word):
    """
    GOOGLE CUSTOM SEARCH APIからキーワードで画像のURLを取得する
    """
    encoded_search_word = urlrequest.quote(search_word)
    url = URL_TEMPLATE.format(key=CUSTOM_SEARCH_API_KEY, cx=CUSTOM_ENGINE_ID, search_word=encoded_search_word)
    req = urlrequest.Request(url)
    res = urlrequest.build_opener(urlrequest.HTTPHandler()).open(req)
    data = json.load(res)

    if "items" not in data:
        return []

    links = []
    for item in data["items"]:
        links.append(item["link"])
    return links

def post(payload):
    """
    SlackにメッセージをPOSTする
    """
    payload_json = json.dumps(payload)
    data = urlencode({"payload": payload_json})
    req = urlrequest.Request(SLACK_POST_URL)
    response = urlrequest.build_opener(urlrequest.HTTPHandler()).open(req, data.encode('utf-8')).read()
    return response.decode('utf-8')

def build_message(url, *args):
    """
    Slack用のメッセージを作成
    """
    post_message = {}
    post_message["text"] = args[0] + url
    return post_message

def get_search_word():
    """
    検索ワードを複数候補の中からランダムに選択する
    """
    members = []
    members.append("白石麻衣")
    members.append("若月佑美")
    members.append("西野七瀬")
    members.append("齋藤飛鳥")
    members.append("秋元真夏")
    members.append("生田絵梨花")
    members.append("生駒里奈")
    members.append("堀未央奈")
    # members.append("乃木坂46")
    return random.choice(members)

def lambda_handler(event, context):
    """
    lambdaの実行
    """
    search_word = get_search_word()
    post_image_to_slack(search_word)
