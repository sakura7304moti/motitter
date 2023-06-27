"""
Flask Server
"""
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from src import sqlite
from src import const
import math

config = const.api_option()
PAGE_SIZE = config.PAGE_SIZE


@app.route("/twitter/search", methods=["POST"])
def search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("page_no", 1)
    page_size = json_data.get("page_size", 40)
    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search()関数を呼び出し
    records = sqlite.search(
        page_no, page_size, hashtag, start_date, end_date, user_name, min_like, max_like
    )

    # search_count()関数を呼び出し
    count = sqlite.search_count(
        hashtag, start_date, end_date, user_name, min_like, max_like
    )
    totalPages = math.ceil(count / page_size)

    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        ),
        "totalPages": totalPages,
    }

    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    response = jsonify(json_data)
    return response


@app.route("/twitter/search/count", methods=["POST"])
def search_count_handler():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得

    # JSONデータから必要なパラメータを抽出
    hashtag = json_data.get("hashtag", "")
    start_date = json_data.get("start_date", "")
    end_date = json_data.get("end_date", "")
    user_name = json_data.get("user_name", "")
    min_like = json_data.get("min_like", 0)
    max_like = json_data.get("max_like", 0)

    # search_count()関数を呼び出し
    count = sqlite.search_count(
        hashtag, start_date, end_date, user_name, min_like, max_like
    )

    # レスポンスとして結果を返す
    response = jsonify(count=count)
    return response


@app.route("/twitter/hololist", methods=["GET"])
def get_hololist():
    json_data = json.dumps(const.holoList(), ensure_ascii=False)
    response = jsonify(json_data)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
