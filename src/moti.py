from . import downloader
from . import utils
from . import const

output = const.Output()
holoList = const.holoList()

from tqdm import tqdm

#scraper
class Scraper:
    def base_scraper(query: str,date:int = 30,limit:int=3000):
        csv_path = utils.get_base_twitter_df(query,date,limit)
        return csv_path

    def holo_scraper(date:int = 30,limit:int=3000):
        for query in tqdm(holoList, desc="query"):
            csv_path = utils.get_holo_twitter_df(query,date,limit)
            downloader.image_download(csv_path)

    def user_scraper(query: str,date:int = 30,limit:int=3000):
        csv_path = utils.get_user_twitter_df(query,date,limit)
        return csv_path
scraper = Scraper()

#downloader
class Downloader:
    def base_downloader(csv_path:str):
        downloader.image_download(csv_path)

    def holo_downloader():
        for query in tqdm(holoList, desc="query"):
            csv_path = output.holo_database(query)
            downloader.image_download(csv_path)

    def user_downloader(csv_path:str):
        downloader.image_download(csv_path)
downloader = Downloader()

#main
class getter:
    def base_getter(query: str,date:int = 30,limit:int=3000):
        csv_path = scraper.base_scraper(query,date,limit)
        downloader.base_downloader(csv_path)

    def holo_getter(date:int = 30,limit:int=3000):
        scraper.holo_scraper(date,limit)
        downloader.holo_downloader()

    def user_getter(query: str,date:int = 30,limit:int=3000):
        csv_path = scraper.user_scraper(query,date,limit)
        downloader.user_downloader(csv_path)