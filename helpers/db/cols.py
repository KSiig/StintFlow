import pymongo
import os
from dotenv import load_dotenv

myclient = pymongo.MongoClient(os.getenv('MONGODB_HOST'))

races_db = myclient["races"]
stints_col = races_db["stints"]
events_col = races_db["events"]
sessions_col = races_db["sessions"]