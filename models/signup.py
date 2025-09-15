from pydantic import BaseModel, constr
from typing import Literal, Union, Optional

from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional, Literal


class LatLong(BaseModel):
    lat: float
    long: float
    address: str

class Farmer(BaseModel):
    role: Literal["farmer"]
    farmer_id: Optional[str]
    name: str
    phone_number: str
    location: Optional[LatLong]
    land_records: Optional[str]  
    certifications: Optional[List[str]] = []
    registered_crops: Optional[List[str]] = []
    aadhar_number: str

class WildCollector(BaseModel):
    role: Literal["wild_collector"]
    wild_collector_id: str
    name: str
    phone_number: str
    location: Optional[LatLong]
    license_no: Optional[str]
    area_assigned: Optional[str]
    certifications: Optional[List[str]] = []
    registered_species: Optional[List[str]] = []
    company_email: EmailStr

class Processor(BaseModel):
    role: Literal["processor"]
    processor_id: str
    company_name: str
    authority_name: str
    address: str
    license_no: Optional[str]
    responsible_person: Optional[str]
    certification_status: Optional[List[str]] = []
    facilities: Optional[List[str]] = []  
    company_email: EmailStr
    phone_number: str

class Laboratory(BaseModel):
    role: Literal["laboratory"]
    lab_id: str
    company_name: str
    location: str
    accreditation_no: Optional[str]
    test_capabilities: Optional[List[str]] = []
    company_email: EmailStr
    ayush_certificate: Optional[List[str]] = []
    phone_number: str

class Manufacturer(BaseModel):
    role: Literal["manufacturer"]
    manufacturer_id: str
    name: str
    address: str
    license_no: Optional[str]
    GMP_certified: Optional[bool]
    company_email: EmailStr
    phone_number: str

class Packer(BaseModel):
    role: Literal["packer"]
    packer_id: str
    name: str
    lic_no: Optional[str]
    location: Optional[str]
    phone_number: str
    company_email: EmailStr

class Storage(BaseModel):
    role: Literal["storage"]
    storage_id: str
    facility_name: str
    location: str
    cert_status: Optional[str]  
    company_email: EmailStr

#SCM LOGIN
class LoginRequest(BaseModel):
    company_email: EmailStr
    password: str
