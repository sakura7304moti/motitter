from src import moti
from src import utils

try:
    model = moti.Downloader()
    model.holo_downloader()
except Exception as e:
    print(e)
    utils.message(e)
