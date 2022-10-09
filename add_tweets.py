from database import Database
from api import get_user, get_timeline
from tqdm import tqdm
from read_config import CONFIG

db = Database(CONFIG["MongoDBServer"]["connect_string"])
# get all user ids from the database
user_ids = db.accounts_db.find({}, {"id": 1}).sort(
    [("last_checked", 1), ("connections", -1)]
)
count = db.accounts_db.count_documents({})
for user_id in tqdm(user_ids, total=count):
    user = get_user(user_id["id"])
    timeline = get_timeline(user, since_id=db.get_last_tweet_id(user))
    db.add_timeline(timeline)
    # update user's last_checked field to now
    db.checked_user(user)
