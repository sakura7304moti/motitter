# Import--------------------------------------------------
import time
import os
import urllib
import datetime

# import timeout_decorator as td
import shutil
import pandas as pd
from tqdm import tqdm
from src import const
import sys
import ast
from . import utils

# Option--------------------------------------------------
output = const.Output()


# Sub Funtion--------------------------------------------------
# URLを指定して画像を保存する
def download(url, save_path):
    try:
        if not os.path.exists(save_path):
            try:
                response = urllib.request.urlopen(url, timeout=10)
            except Exception as e:
                pass
            else:
                if response.status == 200:
                    try:
                        with open(save_path, "wb") as f:
                            f.write(response.read())
                            time.sleep(0.5)
                    except Exception as e:
                        pass
    except Exception as e:
        pass
    finally:
        if os.path.exists(save_path):
            if os.path.getsize(save_path) == 0:
                os.remove(save_path)


# 画像保存先を取得
def get_save_path(url, mode, query):
    file_name = url.split("/")[-1].split("?")[0] + ".jpg"
    if mode == "base":
        save_path = os.path.join(output.base_image(query), file_name)
    if mode == "holo":
        save_path = os.path.join(output.holo_image(query), file_name)
    if mode == "user":
        save_path = os.path.join(output.user_image(query), file_name)
    folder = os.path.dirname(save_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return save_path


# Main Function--------------------------------------------------
def image_download(query, mode, tweet_df):
    utils.message(f"download start -> {query}")
    tweet_df["images"] = [
        ast.literal_eval(d) for d in tweet_df["images"]
    ]  # images str -> list[str]

    saved = 0
    for index, row in tqdm(
        tweet_df.iterrows(), total=len(tweet_df), desc="image DL"
    ):  # 画像のダウンロード&保存処理
        images = row["images"]
        for url in images:
            save_path = get_save_path(url, mode, query)
            if not os.path.exists(save_path):
                try:
                    download(url, save_path)
                except Exception as e:
                    print(e)
                    pass
    utils.message(f"download finish -> {query} | saved : {saved}")
