# src/mongo_dal.py
from pymongo import MongoClient, ReturnDocument

class MongoDAL:
    def __init__(self, uri="mongodb+srv://maliksaqlain4785:hacker@cluster0.xisyedz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name="airline"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.loyalty = self.db["loyalty_profiles"]

    # ----------------------------
    # Loyalty Profile CRUD
    # ----------------------------
    def create_loyalty_profile(self, passenger_id, tier="Bronze", points=0, feedback=None):
        profile = {
            "passenger_id": passenger_id,
            "tier": tier,
            "points": points,
            "feedback": feedback or []
        }
        self.loyalty.insert_one(profile)
        # return the created profile (without Mongo _id)
        return {k: v for k, v in profile.items()}

    def get_loyalty_profiles(self):
        return list(self.loyalty.find({}, {"_id": 0}))  # hide Mongo _id for cleaner output

    def add_feedback(self, passenger_id, comment):
        return self.loyalty.find_one_and_update(
            {"passenger_id": passenger_id},
            {"$push": {"feedback": {"comment": comment}}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 0}  # hide _id
        )

    def update_points(self, passenger_id, points):
        return self.loyalty.find_one_and_update(
            {"passenger_id": passenger_id},
            {"$inc": {"points": points}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 0}  # hide _id
        )

    def delete_loyalty_profile(self, passenger_id):
        result = self.loyalty.delete_one({"passenger_id": passenger_id})
        return {"deleted_count": result.deleted_count}
