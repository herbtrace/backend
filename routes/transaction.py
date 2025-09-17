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
import requests

load_dotenv()

router = APIRouter(tags = ["Transactions"])
MONGO_URI = os.getenv("MONGO_URI")
# BC_URI = "http://localhost:4000"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["supply_chain"]
crops_collection = db["crops"]

@router.post("/start")
def add_crop(response : FarmerDetails):
    data={'batch_id': response.batch_id,
          'crop_id': response.crop_id,
          'start_time': response.start_time
          }
    try:
        result = crops_collection.update_one(
            {},
            {"$push": {f"farmer.{response.profile_id}": data}},
            upsert=True
        )
        return {"message": "Crop added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get")
def get_profile_data(profile_id: str, role: str):
    doc = crops_collection.find_one(
    { f"{role.lower()}.{profile_id}": { "$exists": True } },
    { f"{role.lower()}.{profile_id}": 1, "_id": 0 }
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc.get(role.lower() , {}).get(profile_id, [])

@router.post("/transactions")
def validate(response : QrCodeData):

    # try:
    #     requests.post(f"{BC_URI}/event", json=response.event.dict())
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Blockchain interaction failed")
    
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
    
    return {"message": "Transaction successful"}

