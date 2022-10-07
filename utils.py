from tqdm import tqdm
from api import api, get_user


def add_friends(user, database, add_tweets=True):
    """
    Finds and adds friends of a user to the database.
    """
    for friend_id in tqdm(api.get_friend_ids(user_id=user.id)):
        friend = get_user(user_id=friend_id)
        is_new = database.add_account(friend)
        if is_new and add_tweets and not friend.protected:
            for tweet in friend.timeline():
                database.add_tweet(tweet)

    database.accounts_db.update_one({"id": user.id}, {"$set": {"friends_added": True}})
