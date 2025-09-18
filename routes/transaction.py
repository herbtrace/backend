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
    escaped_profile_id = profile_id.replace('.', '\u002e').replace('$', '\u0024')
    doc = crops_collection.find_one(
    { f"{role}": { "$exists": True }, f"{role}.{escaped_profile_id}": { "$exists": True } })

    print(role, profile_id, doc)
    if not doc:
       return []
    return doc.get(role, {}).get(profile_id, [])

@router.post("/transactions")
def validate(response : QrCodeData):

    data={'batch_id': response.batch_id,
        #   'crop_id': doc['crop_id'],
          'start_time': response.start_time}

    doc= crops_collection.find()
    # # print(doc)
    for d in doc:
        
        for item in d.get(response.from_role, {}).get(response.from_id, []):
            # print(item)
            # print('_'*100)
            # print(item['batch_id'], data['batch_id'])
            if item['batch_id']==data['batch_id']:
                doc=item
                print("Found:", doc)
                break
        else:
            doc=None
    if not doc:
        raise HTTPException(status_code=404, detail="No matching batch found")

    crops_collection.update_one(
    {},
    {"$pull": {
        f"{response.from_role}.{response.from_id}": {
            "batch_id": data["batch_id"]
        }
    }}
)
    data={'batch_id': response.batch_id,
          'crop_id': doc['crop_id'],
          'start_time': response.start_time}
    
    crops_collection.update_one(
        {},
        {"$push": {f"{response.to_role}.{response.to_id}": data}},
        upsert=True
    )    
    
    return {"message": "Transaction successful"}

