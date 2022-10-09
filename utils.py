from tqdm import tqdm
from api import api, get_user


def add_timeline(user, database):
    """
    Adds user timeline to the dataset
    """
    timeline = user.timeline(tweet_mode= "extended")
    database.add_timeline(timeline)
    database.checked_user(user) 

def add_friends(user, database, add_tweets=True):
    """
    Finds and adds friends of a user to the database.
    """
    for friend_id in tqdm(api.get_friend_ids(user_id=user.id)):
        friend = get_user(user_id=friend_id)
        is_new = database.add_account(friend)
        if add_tweets and is_new and not friend.protected:
            add_timeline(friend, database)

    database.accounts_db.update_one({"id": user.id}, {"$set": {"friends_added": True}})
