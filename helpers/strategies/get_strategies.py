from helpers.db.cols import strategies_col
from bson import ObjectId

def get_strategies(session_id):
    return strategies_col.find({"session_id": ObjectId(session_id)})