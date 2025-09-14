from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from typing import Literal, Union, Optional
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["supply_chain"]
profiles_collection = db["profiles"]

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Login Schemas
class BaseProfile(BaseModel):
    name: str
    phone_number: str

class Farmer(BaseProfile):
    role: Literal["farmer"]
    aadhaar_id: Optional[str]
    location: str
    password: constr(pattern=r"^\d{4}$") 

class Transporter(BaseProfile):
    role: Literal["transporter"]
    vehicle_id: str
    license_no: Optional[str]
    password: constr(min_length=8)

class ProcessingUnit(BaseProfile):
    role: Literal["processing_unit"]
    location: str
    license_no: str
    contact_person: str
    password: constr(min_length=8)

class QualityLab(BaseProfile):
    role: Literal["quality_lab"]
    lab_name: str
    location: str
    license_accreditation_no: str
    contact_person: str
    password: constr(min_length=8)

class PackagingDept(BaseProfile):
    role: Literal["packaging_dept"]
    company_name: str
    location: str
    license_no: str
    contact_person: str
    password: constr(min_length=8)

class LoginRequest(BaseModel):
    phone_number: str
    password: str
    role: str

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

    

