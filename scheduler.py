from src import moti,const

model = moti.Getter()
option = const.option_sc()
tag = const.hashtags()
"""
BASE
"""
date,limit = option.base_option()
hashtags = tag.base_hashtags()
for p in hashtags:
    model.base_getter(p,date,limit)
"""
HOLO
"""
date,limit = option.holo_option()
hashtags = tag.holo_hashtags()
for p in hashtags:
    model.holo_getter(p,date,limit)
"""
USER
"""
date,limit = option.user_option()
hashtags = tag.user_hashtags()
for p in hashtags:
    model.user_getter(p,date,limit)