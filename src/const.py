import os
import pandas as pd
import yaml

# プロジェクトの相対パス
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# hololive fanart tag list
def holoList():
    holo_path = os.path.join(base_path, "option", "HoloFanArt.csv")
    df = pd.read_csv(holo_path, index_col=0)
    word_list = df["FanArt"].tolist()
    return word_list


def _output() -> dict:
    yaml_path = os.path.join(base_path, "option", "output.yaml")
    with open(yaml_path) as file:
        yml = yaml.safe_load(file)
    return yml


class Output:
    def __init__(self):
        self._base_path = base_path
        self._yml = _output()
        # make folders
        if not os.path.exists(self._yml["base"]["database"]):
            os.makedirs(self._yml["base"]["database"])
        if not os.path.exists(self._yml["base"]["image"]):
            os.makedirs(self._yml["base"]["image"])

        if not os.path.exists(self._yml["holo"]["database"]):
            os.makedirs(self._yml["holo"]["database"])
        if not os.path.exists(self._yml["holo"]["image"]):
            os.makedirs(self._yml["holo"]["image"])

        if not os.path.exists(self._yml["user"]["database"]):
            os.makedirs(self._yml["user"]["database"])
        if not os.path.exists(self._yml["user"]["image"]):
            os.makedirs(self._yml["user"]["image"])

    def base_database(self, query: str):
        return os.path.join(
            self._base_path, self._yml["base"]["database"], f"{query}_database.csv"
        )

    def base_image(self, query: str):
        return os.path.join(self._base_path, self._yml["base"]["image"], f"{query}")

    def holo_database(self, query: str):
        return os.path.join(
            self._base_path, self._yml["holo"]["database"], f"{query}_database.csv"
        )

    def holo_image(self, query: str):
        return os.path.join(self._base_path, self._yml["holo"]["image"], f"{query}")

    def user_database(self, userName: str):
        return os.path.join(
            self._base_path, self._yml["user"]["database"], f"{userName}_database.csv"
        )

    def user_image(self, userName: str):
        return os.path.join(self._base_path, self._yml["user"]["image"], f"{userName}")

#Option--------------------------------------------------
class options:
    limit_date = 30
    limit_tweets = 3000