# Import--------------------------------------------------
import pandas as pd
from tqdm import tqdm

# import snscrape.modules.twitter as sntwitter
from .snscrape import twitter as sntwitter
import time
import os
import urllib
import datetime
import yaml
import sys
from pathlib import Path
import shutil
import requests

# sub import--------------------------------------------------
from . import const

output = const.Output()
options = const.options()


# sub function--------------------------------------------------
# optionを更新する
def update_options(date=30, limit=3000):
    options.limit_date = date
    options.limit_tweets = limit
    print(f"update -> date : {options.limit_date} ,\n limit : {options.limit_tweets}")


# ツイートを取得
def get_tweets(query: str, mode: str):
    print(f"start {query}...")
    message(f"search start -> {query}")
    if mode == "user":
        scraper = sntwitter.TwitterUserScraper(query)
    else:
        scraper = sntwitter.TwitterSearchScraper(query)
    tweets = []
    today = datetime.datetime.today()
    for index, tweet in enumerate(scraper.get_items()):
        images = []
        # スパム対策で高評価4以上のみ取得
        if tweet.likeCount > 4:
            try:
                for media in tweet.media:
                    images.append(media.fullUrl)

                data = [
                    tweet.url,  # ツイート元URL
                    [media.fullUrl for media in tweet.media],  # 画像URL
                    tweet.date,  # ツイート日時
                    tweet.user.username,  # ツイートした人のid
                    tweet.user.displayname,  # ツイートした人の名前
                    tweet.likeCount,  # 高評価数
                ]
                if len(tweet.media) > 0:
                    tweets.append(data)
            except:
                pass

        # ツイートと今日の日付がlimit_date日以上の差があれば終了
        rep_date = tweet.date.replace(tzinfo=None)
        if (today - rep_date).days >= options.limit_date:
            break

        # limit_tweets枚を上限(時間がかかるため)
        if len(tweets) > options.limit_tweets:
            break

        # 進捗print
        if len(tweets) % 100 == 0 and len(tweets) > 0:
            print("\rTweet count : {0}".format(len(tweets)), end="")

    # breakしたら、データフレームにして保存する
    tweet_df = pd.DataFrame(
        tweets, columns=["url", "images", "date", "userId", "userName", "likeCount"]
    )
    message(f"search finish -> {query}")
    return tweet_df


# データフレームをマージする
def marge_dataframe(tweet_df, csv_path):
    if os.path.exists(csv_path):
        before_df = pd.read_csv(csv_path, index_col=None)
        marged = pd.merge(tweet_df, before_df, on="url", how="outer")

        # 結合後のデータフレームの列を条件にしてデータを更新する
        marged["date"] = marged["date_y"].fillna(marged["date_x"])
        marged["images"] = marged["images_y"].fillna(marged["images_x"])
        marged["userId"] = marged["userId_y"].fillna(marged["userId_x"])
        marged["userName"] = marged["userName_x"].fillna(marged["userName_y"])
        marged["likeCount"] = marged["likeCount_x"].fillna(marged["likeCount_y"])

        result = marged[
            ["url", "date", "images", "userId", "userName", "likeCount"]
        ]  # 結合後のデータフレーム
        return result
    else:
        return tweet_df


def message(text: str):
    try:
        # 取得したTokenを代入
        line_notify_token = "bLg2L6w7MhUXm5eG1Pyz6jB5IJ8PVU3anYX5FbjUbSc"

        # 送信したいメッセージ
        message = text

        # Line Notifyを使った、送信部分
        line_notify_api = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        data = {"message": f"{message}"}
        requests.post(line_notify_api, headers=headers, data=data)
    except:
        pass


# main function--------------------------------------------------------------------------------------------
def get_df(query: str, mode: str, date: int = 30, limit: int = 3000):
    update_options(date, limit)
    df = get_tweets(query, mode)
    if mode == "base":
        csv_path = output.base_database(query)
    if mode == "holo":
        csv_path = output.holo_database(query)
    if mode == "user":
        csv_path = output.user_database(query)
    marge_dataframe(df, csv_path).to_csv(csv_path)
    return df


def get_base_twitter_df(query: str, date: int = 30, limit: int = 3000):
    df = get_df(query, "base", date, limit)
    return df


def get_holo_twitter_df(query: str, date: int = 30, limit: int = 3000):
    df = get_df(query, "holo", date, limit)
    return df


def get_user_twitter_df(query: str, date: int = 30, limit: int = 3000):
    df = get_df(query, "user", date, limit)
    return df
