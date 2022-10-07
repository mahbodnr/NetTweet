import tweepy
import time
from datetime import datetime
from read_config import CONFIG

api_key = CONFIG["TwitterDevAPI"]["api_key"]
api_key_secret = CONFIG["TwitterDevAPI"]["api_key_secret"]
access_toke = CONFIG["TwitterDevAPI"]["access_toke"]
access_toke_secret = CONFIG["TwitterDevAPI"]["access_toke_secret"]


auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_toke, access_toke_secret)
api = tweepy.API(auth)


def tweepy_error_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tweepy.errors.TooManyRequests:
            print(
                f"Rate limit exceeded at {datetime.now().strftime('%H:%M')}. Waiting 15 minutes."
            )
            time.sleep(15 * 60 + 1)
            return func(*args, **kwargs)
        except tweepy.errors.Unauthorized:
            print(f"Unauthorized Error. user profile is private.")
            return
        except Exception as e:
            raise Exception(e)

    return wrapper


@tweepy_error_check
def get_user(user_id):
    return api.get_user(user_id=user_id)


@tweepy_error_check
def get_timeline(user, count=50, since_id=None):
    return api.user_timeline(
        user_id=user.id,
        tweet_mode="extended",
        count=count,
        since_id=since_id,
        exclude_replies=True,
    )
