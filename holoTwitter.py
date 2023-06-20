from src import moti
from src import utils

try:
    model = moti.Getter()
    model.holo_getter(14, 10000)
except Exception as e:
    print(e)
    utils.message(e)
