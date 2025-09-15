from fastapi import APIRouter, HTTPException
from typing import Union
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from models.signup import (
    Farmer,
    WildCollector,
    Processor,
    Laboratory,
    Manufacturer,
    Packer,
    Storage,
    LoginRequest
)
import uuid

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["supply_chain"]
profiles_collection = db["profiles"]

router = APIRouter(prefix="/profiles", tags=["Profiles"])

ProfileUnion = Union[Farmer, WildCollector, Processor, Laboratory,Manufacturer, Packer, Storage]

@router.post("/create")
def create_profile(profile: ProfileUnion):
    try:
        if profile.role == "farmer":
            existing = profiles_collection.find_one({
                "role": profile.role,
                "phone_number": profile.phone_number
            })
        else:
            existing = profiles_collection.find_one({
                "role": profile.role,
                "company_email": profile.company_email
            })
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"{profile.role.capitalize()} already exists"
            )
        auth=str(uuid.uuid4())
        profile_dict = profile.dict()
        profile_dict["auth_token"] = auth

        result = profiles_collection.insert_one(profile.dict())
        return {
            "id": str(result.inserted_id),
            "role": profile.role,
            "msg": f"{profile.role.capitalize()} profile created successfully"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# SCM LOGIN  
@router.post("/login")
async def login(data: LoginRequest):
    email = data.company_email
    password = data.password

    if password is None or email is None:
        raise HTTPException(status_code=400, detail="Email and password are required")

    if password == "scm@123" and email == "scm@example.com":
        return {
            "company_email": email,
            "role": "scm",
            "msg": "SCM login successful",
            "auth_token": str(uuid.uuid4())
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
        
    

    

