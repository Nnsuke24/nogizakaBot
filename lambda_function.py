#-*- coding:utf-8 -*-
from urlparse import urljoin
from urllib import urlencode
import urllib2 as urlrequest
import json
import random

# CUSTOM SEARCH API周りの設定
CUSTOM_SEARCH_API_KEY = "AIzaSyAlpyIw0CuFYuadn3l7s4W64A607f9V_n8"
CUSTOM_ENGINE_ID = "015902463065345753840:g8t7587xada"
URL_TEMPLATE = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&searchType=image&q={search_word}"

# SLACK周りの設定
SLACK_POST_URL = "https://hooks.slack.com/services/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"

def post_image_to_slack(search_word):
    """
    google custom serachでimageのURLを取得し，ランダムでSLACKに投稿する
    """
    # urlを複数取得する
    urls = get_image_urls(search_word)

    # urlが取得できなかった場合は投稿しない
    if len(urls) == 0:
        return "no images were found."

    # urlをランダムに選択する
    url = random.choice(urls)

    # slack用のメッセージを作成
    post_msg = build_message(url)

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

def build_message(url, **kwargs):
    """
    Slack用のメッセージを作成
    """
    post_message = {}
    post_message["text"] = "おはよう！今日も頑張ろう！！\n" + url
    post_message.update(kwargs)
    return post_message


def lambda_handler(event, context):
    """
    lambdaの実行
    検索候補を格納し、その中からランダムに検索ワードを選択する
    """
    members = []
    members.append("白石麻衣")
    members.append("西野七瀬")
    members.append("齋藤飛鳥")
    members.append("秋元真夏")
    members.append("堀未央奈")
    members.append("乃木坂46")
    search_word = random.choice(members)
    
    post_image_to_slack(search_word)