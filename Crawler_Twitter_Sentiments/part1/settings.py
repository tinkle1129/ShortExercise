TRACK_TERMS = ["THAAD"]
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "twitter_message.csv"
TABLE_NAME = "THAAD"

OFFICIAL_LIST=['PDChina','XHNews','YonhapNews', 'cnn','WashTimes']
OFFICIAL_LOC =['CHN','CHN','KOR','USA','USA']#

CSV_NAME_OFFICIAL='twitter_message_official.csv'
TABLE_NAME_OFFICIAL = "THAAD_OFFICIAL"

try:
    from private import *
except Exception:
    pass