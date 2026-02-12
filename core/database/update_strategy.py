"""
Update strategy in MongoDB.

Updates strategy document with new model data.
"""

from bson import ObjectId
from .connection import get_strategies_collection


def update_strategy(strategy_id: str | ObjectId=None, model_data: dict=None, strategy=None) -> None:
    """
    Update strategy with new model data.
    
    Args:
        strategy_id: MongoDB ObjectId as string or ObjectId
        model_data: Sanitized model data with 'rows' and 'tires' keys
    """
    strategies_col = get_strategies_collection()

    if strategy:
        print("rows: ", len(strategy.get('model_data', {}).get('rows', [])))
        strategies_col.update_one(
            {"_id": strategy["_id"]},
            {"$set": {
                "model_data": strategy.get('model_data', {}),
                "mean_stint_time_seconds": strategy.get('mean_stint_time_seconds', None)
                }}
            )
        return

    if isinstance(strategy_id, str):
        strategy_id = ObjectId(strategy_id)
    
    strategies_col.update_one(
        {"_id": strategy_id},
        {"$set": {"model_data": model_data}}
    )
