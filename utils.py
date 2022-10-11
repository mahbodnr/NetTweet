from tqdm import tqdm
from api import api, get_user


def add_timeline(user, database):
    """
    Adds user timeline to the dataset
    """
    timeline = user.timeline(tweet_mode="extended")
    database.add_timeline(timeline)
    database.checked_user(user)


def add_friends(user, database, complete_account=False, add_tweets=False):
    """
    Finds and adds friends of a user to the database.
    """
    if complete_account:
        for friend_id in tqdm(api.get_friend_ids(user_id=user.id)):
            friend = get_user(user_id=friend_id)
            is_new = database.add_account(friend)
            if add_tweets and is_new and not friend.protected:
                add_timeline(friend, database)
    else:
        assert (
            not add_tweets
        ), "'add_tweets' is only available when 'complete_account = True'"
        friend_ids = list(api.get_friend_ids(user_id=user.id))
        for friend_id in tqdm(friend_ids):
            database.add_account_id(friend_id)

    database.accounts_db.update_one({"id": user.id}, {"$set": {"friends_added": True}})
