from src import moti, const, utils

try:
    utils.message("scheduler start")
    model = moti.Getter()
    option = const.option_sc()
    tag = const.hashtags()
    """
    BASE
    """
    date, limit = option.base_option()
    hashtags = tag.base_hashtags()
    for p in hashtags:
        model.base_getter(p, date, limit)
    """
    HOLO
    """
    date, limit = option.holo_option()
    hashtags = tag.holo_hashtags()
    model.holo_getter(date, limit)
    """
    USER
    """
    date, limit = option.user_option()
    hashtags = tag.user_hashtags()
    for p in hashtags:
        model.user_getter(p, date, limit)
    utils.message("scheduler end")
except Exception as e:
    print(e)
    utils.message(e)
