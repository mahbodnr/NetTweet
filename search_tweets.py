from database import Database
from read_config import CONFIG

search_keywords = CONFIG["Search"]["origin_nodes"].split(",")


db = Database(CONFIG["MongoDBServer"]["connect_string"])
print(f"Searching through {db.tweets_db.count_documents({})} tweets.")
search_regex = f"(?i)^.*(^|[^a-zA-Z])({'|'.join(search_keywords)})($|[^a-zA-Z]).*$"

count = db.tweets_db.count_documents({"full_text": {"$regex": search_regex}})
if not count:
    print("No tweet found")
else:
    res = db.tweets_db.find({"full_text": {"$regex": search_regex}})
    with open("tweets.txt", "w", encoding="utf-8") as f:
        for tweet in res:
            tweet_url = f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"
            f.write(tweet["full_text"] + f" ({tweet_url})" + "\n")
        f.flush()
        print(f"Added {count} tweets to tweet.txt")
