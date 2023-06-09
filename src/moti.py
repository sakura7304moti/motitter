from . import download
from . import utils
from . import const
from . import sqlite
import pandas as pd

output = const.Output()
holoList = const.holoList()

from tqdm import tqdm
import os


# scraper
class Scraper:
    def base_scraper(self, query: str, date: int = 30, limit: int = 3000):
        df = utils.get_base_twitter_df(query, date, limit)
        return df

    def holo_scraper(self, date: int = 30, limit: int = 3000):
        for query in tqdm(holoList, desc="query"):
            utils.get_holo_twitter_df(query, date, limit)

    def user_scraper(self, query: str, date: int = 30, limit: int = 3000):
        df = utils.get_user_twitter_df(query, date, limit)
        return df


scraper = Scraper()


# downloader
class Downloader:
    def base_downloader(self, query: str):
        csv_path = output.base_database(query)
        df = pd.read_csv(csv_path)
        download.image_download(query, "base", df)

    def holo_downloader(self):
        for query in tqdm(holoList, desc="query"):
            csv_path = output.holo_database(query)
            df = pd.read_csv(csv_path)
            download.image_download(query, "holo", df)

    def user_downloader(self, query: str):
        csv_path = output.user_database(query)
        df = pd.read_csv(csv_path)
        download.image_download(query, "user", df)


downloader = Downloader()


# main
class Getter:
    def base_getter(self, query: str, date: int = 30, limit: int = 3000):
        scraper.base_scraper(query, date, limit)
        downloader.base_downloader(query)
        csv_path = output.base_database(query)
        sqlite.update(csv_path,'base')

    def holo_getter(self, date: int = 30, limit: int = 3000):
        scraper.holo_scraper(date, limit)
        downloader.holo_downloader()
        for hashtag in holoList:
            csv_path = output.holo_database(hashtag)
            sqlite.update(csv_path,'holo')


    def user_getter(self, query: str, date: int = 30, limit: int = 3000):
        scraper.user_scraper(query, date, limit)
        downloader.user_downloader(query)
        csv_path = output.user_database(query)
        sqlite.update(csv_path,'user')
