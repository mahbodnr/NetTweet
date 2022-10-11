from pymongo import MongoClient
from datetime import datetime
from read_config import CONFIG


class Database:
    def __init__(self, address=r"mongodb://localhost:27017/"):
        self.client = MongoClient(address)
        self.db = self.client[CONFIG["Database"]["cluster_name"]]
        self.accounts_db = self.db["accounts"]
        self.tweets_db = self.db["tweets"]

    def add_account(self, user, add_private=False, increase_connections=True):
        """
        Checks if user id already exists in the database.
        If previously exists, adds number of connections.
        if not adds a new user to the database.

        Return: a bool indicating whether the user was a new record
        """
        if self.accounts_db.find_one({"id": user.id}):
            if increase_connections:
                self.accounts_db.update_one(
                    {"id": user.id}, {"$inc": {"connections": 1}}
                )
            return False
        else:
            if (not user.protected) or add_private:  # check if user is not private
                # add to dataset with a field called last_checked with the date of now
                self.accounts_db.insert_one(
                    {
                        **user._json,
                        "connections": 1,
                        "last_checked": datetime.now(),
                        "friends_added": False,
                    }
                )
            return True

    def add_account_id(self, user_id, increase_connections=True):
        if self.accounts_db.find_one({"id": user_id}):
            if increase_connections:
                self.accounts_db.update_one(
                    {"id": user_id}, {"$inc": {"connections": 1}}
                )
            return False
        else:
            # add to dataset with a field called last_checked with the date of now
            self.accounts_db.insert_one(
                {
                    "id": user_id,
                    "connections": 1,
                    "last_checked": datetime.now(),
                    "friends_added": False,
                }
            )
            return True

    def update_account(self, user):
        self.accounts_db.update({"_id": user.id}, {"$set": {**user._json}})

    def add_tweet(self, tweet):
        if not self.tweets_db.find_one({"id": tweet.id}):
            self.tweets_db.insert_one(tweet._json)

    def checked_user(self, user):
        self.accounts_db.update_one(
            {"id": user.id}, {"$set": {"last_checked": datetime.now()}}
        )

    def add_timeline(self, timeline):
        for tweet in timeline:
            self.add_tweet(tweet)

    def get_last_tweet_id(self, user):
        count = self.accounts_db.count_documents({"user.id": user.id})
        if count:
            return self.tweets_db.find({"user.id": user.id}).sort("id", -1)[0]["id"]
        else:
            return None
