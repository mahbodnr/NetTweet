from database import Database
from api import api
from datetime import datetime
from read_config import CONFIG
from utils import add_friends, add_timeline

db = Database(CONFIG["MongoDBServer"]["connect_string"])
origin_nodes = CONFIG["Search"]["origin_nodes"].split(",")

for user_screen_name in origin_nodes:
    user = api.get_user(screen_name=user_screen_name)
    is_new = db.add_account(user, increase_connections=False)
    if is_new and not user.protected:
        add_timeline(user, db)
    print(
        f"Adding {user.name}'s friends. Started at: {datetime.now().strftime('%H:%M')}"
    )
    add_friends(user, db, add_tweets=True)

print("Origin Nodes have been added to the database.")
