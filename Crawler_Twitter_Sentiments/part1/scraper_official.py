import settings
import tweepy
import dataset
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from sqlalchemy.exc import ProgrammingError

db = dataset.connect(settings.CONNECTION_STRING)
auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

for user_name,user_loc in zip(settings.OFFICIAL_LIST,settings.OFFICIAL_LOC):
    user = api.get_user(user_name)
    p = 1

    while (p <= 200 and len(user.timeline(page=p))):
        print p
        public_tweets = user.timeline(page=p)
        for tweet in public_tweets:
            flag = 0
            if 'THAAD' in tweet.text:
                flag = 1
            if 'thaad' in tweet.text:
                flag = 1
            if flag ==1:
                loc = tweet.user.location
                text = tweet.text
                created_at = tweet.created_at
                blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
                sent = blob.sentiment
                table = db[settings.TABLE_NAME_OFFICIAL]
                try:
                    table.insert(dict(
                        user_location=loc,
                        text=text,
                        p_pos=sent.p_pos,
                        p_neg=sent.p_neg,
                        created_at=created_at,
                        user_name = user_name,
                        user_loc = user_loc
                    ))
                    print loc,sent
                except ProgrammingError as err:
                    print(err)
        p = p + 1
