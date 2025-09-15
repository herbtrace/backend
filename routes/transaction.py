from fastapi import APIRouter, HTTPException
import json
import datetime
# from geopy.geocoders import Nominatim
from models.stages import QrCodeData, CollectionEvent, FarmerDetails
from typing import List
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix = "/transactions", tags = ["Transactions"])
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["supply_chain"]
crops_collection = db["crops"]

# def state(latitude,longitude):
#     geolocator = Nominatim(user_agent="crop_app")
#     location = geolocator.reverse((latitude, longitude), exactly_one=True)

#     return location.raw['address']['state']

# with open ("validation.json") as f:
#         plant_data=json.load(f)

@router.post("/get")
def get_farmer_data(profile_id: str, role: str):
    doc = crops_collection.find_one(
    { f"{role}.{profile_id}": { "$exists": True } },
    { f"{role}.{profile_id}": 1, "_id": 0 }
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return doc

@router.post("/validate")
def validate(response : QrCodeData):
    data={'batch_id': response.event.batch_id,
          'crop_id': response.event.crop_id,
          'start_time': response.start_time}
    

    crops_collection.update_one(
        {},
        {"$push": {f"{response.to_role}.{response.to_id}": data}},
        upsert=True
    )    

    crops_collection.update_one(
    {},
    {"$pull": {
        f"{response.from_role}.{response.from_id}": {
            "batch_id": data["batch_id"],
            "crop_id": data["crop_id"]
        }
    }}
)
    for doc in crops_collection.find():
        print(doc)

    # Blockchain interaction to be added here
    return {"message": "Transaction successful"}

@router.post("/start")
def add_crop(response : CollectionEvent):
    data={'batch_id': response.batch_id,
          'crop_id': response.crop_id,
          'start_time': response.start_date,
          }
    try:
        result = crops_collection.update_one(
            {},
            {"$push": {f"farmer.{response.actor_id}": data}},
            upsert=True
        )
        return {"message": "Crop added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))