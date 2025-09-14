from fastapi import APIRouter, HTTPException
from typing import Union
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from models.signup import (
    Farmer,
    Transporter,
    PackagingDept,
    ProcessingUnit,
    QualityLab,
    LoginRequest
)


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["supply_chain"]
profiles_collection = db["profiles"]

router = APIRouter(prefix="/profiles", tags=["Profiles"])

ProfileUnion = Union[Farmer, Transporter, ProcessingUnit, QualityLab, PackagingDept]


@router.post("/create")
def create_profile(profile: ProfileUnion):
    try:
        existing = profiles_collection.find_one({
            "role": profile.role,
            "phone_number": profile.phone_number
        })
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"{profile.role.capitalize()} already exists"
            )

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
    
@router.post("/login")
async def login(data: LoginRequest):
    phone = data.phone_number
    password = data.password
    role = data.role

    user_db = profiles_collection.find_one({"phone_number": phone, "role": role})
    if not user_db:
        raise HTTPException(status_code=401, detail="User not found")

    if user_db["password"] == password:
        return {"message": "Login successful", "role": role}
    else:
        raise HTTPException(status_code=401, detail="Invalid PIN")

    

