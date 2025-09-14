from pydantic import BaseModel, constr
from typing import Literal, Union, Optional

# Signup models
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

