import argparse
from database import Database
from api import api, get_user
from datetime import datetime
from read_config import CONFIG
from utils import add_friends

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "--add-tweets",
    type=bool,
    required=False,
    default=False,
    help="Add new nodes' tweets to the database as well",
)
ap.add_argument(
    "--complete-accounts",
    type=bool,
    required=False,
    default=False,
    help="Always add accounts with full information when adding a new node (slow).",
)
args = vars(ap.parse_args())

# Connect to the database
db = Database(CONFIG["MongoDBServer"]["connect_string"])

# Check database for users with friends_added = False and sort them based on connections
scholars = db.accounts_db.find({"friends_added": False}).sort("connections", -1)
count = db.accounts_db.count_documents({"friends_added": False})
# Check if there is any data in scholars
while count > 0:
    # get the first item in scholars
    for scholar in scholars:
        user = get_user(scholar["id"])
        db.update_account(user)
        print(
            f"Adding {user.name}'s friends. Started at: {datetime.now().strftime('%H:%M')}"
        )
        add_friends(
            user,
            db,
            complete_account=args["complete_accounts"],
            add_tweets=args["add_tweets"],
        )
        break
    scholars = db.accounts_db.find({"friends_added": False}).sort("connections", -1)
    count = db.accounts_db.count_documents({"friends_added": False})
else:
    print("All users have been added to the database")
