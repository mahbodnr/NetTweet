from database import Database
from api import api, get_user
from datetime import datetime
from read_config import CONFIG
from utils import add_friends

db = Database(CONFIG["MongoDBServer"]["connect_string"])

# Check database for users with friends_added = False and sort them based on connections
scholars = db.accounts_db.find({"friends_added": False}).sort("connections", -1)
count = db.accounts_db.count_documents({"friends_added": False})
# Check if there is any data in scholars
while count > 0:
    # get the first item in scholars
    for scholar in scholars:
        user = get_user(scholar["id"])
        print(
            f"Adding {user.name}'s friends. Started at: {datetime.now().strftime('%H:%M')}"
        )
        add_friends(user, db, add_tweets=True)
        break
    scholars = db.accounts_db.find({"friends_added": False}).sort("connections", -1)
    count = db.accounts_db.count_documents({"friends_added": False})
else:
    print("All users have been added to the database")
