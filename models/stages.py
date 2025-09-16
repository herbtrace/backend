from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime


# 🔹 Common Objects
class LatLong(BaseModel):
    lat: float
    long: float
    address: Optional[str]

class EnvironmentalConditions(BaseModel):
    soil_quality: Optional[str]
    moisture: Optional[float]
    temperature: Optional[float]
    humidity: Optional[float]
    weather_conditions: Optional[str]
    irrigation_method: Optional[str]


class FarmingInputs(BaseModel):
    fertilizers: Optional[str]
    pesticides_used: Optional[str]
    organic_certified: bool = False


class PermitCompliance(BaseModel):
    permit_id: str
    permit_type: str
    issuer: str
    valid_until: Optional[datetime]

class FarmerDetails(BaseModel):
    farmer_id: str
    batch_id: str
    crop_id: str
    start_time : datetime

# a. Collection Event
class CollectionEvent(BaseModel):
    batch_id: str
    actor_id: str 
    crop_id: str   
    location: LatLong
    start_date: datetime
    harvest_date: datetime
    environment: Optional[EnvironmentalConditions]
    inputs: Optional[FarmingInputs]
    permits: Optional[List[PermitCompliance]]


#  b. Transport Event
class TransportEvent(BaseModel):
    transport_id: str
    batch_ids: List[int]
    provenance_fhir_url: HttpUrl
    transporter_id: str
    origin: LatLong
    destination: LatLong
    start_time: datetime
    end_time: datetime
    transport_conditions: Optional[EnvironmentalConditions]
    sealed: bool = True
    notes: Optional[str]


#  c. Processing Event
class ProcessingEvent(BaseModel):
    processing_id: str
    batch_id: str
    processing_company_id: str
    company_location: LatLong
    processes_applied: List[str]
    process_conditions: Optional[EnvironmentalConditions]
    start_time: datetime
    end_time: datetime
    visual_inspection: Optional[List[str]]
    equipment_cleaned: bool = True
    notes: Optional[str]


#  d. Quality Test
class TestResults(BaseModel):
    test_id: str
    test_type: str
    value: float
    units: str
    reference_range: Optional[str]
    passed: bool


class QualityTest(BaseModel):
    test_id: str
    batch_id: str
    lab_id: str
    date_of_test: datetime
    test_results: List[TestResults]
    certification_report_url: Optional[HttpUrl]
    notes: Optional[str]


#  Manufacturing Event
class IngredientsModel(BaseModel):
    ingredient_id: str
    name: str
    quantity: float
    units: str


class ManufacturingEvent(BaseModel):
    manufacturing_id: str
    product_name: str
    batch_ids_used: List[int]
    manufacturer_id: str
    manufacture_date: datetime
    ingredients: List[IngredientsModel]
    GMP_compliance: bool = True
    test_ids: Optional[List[str]]
    final_quantity: float
    notes: Optional[str]


#  Packing Event
class PackingEvent(BaseModel):
    packing_id: str
    packing_fhir_url: HttpUrl
    manufacturing_id: str
    packer_id: str
    date_of_packing: datetime
    qr_code_url: Optional[HttpUrl]
    notes: Optional[str]

class QrCodeData(BaseModel):
    from_id: str
    to_id: str  
    crops: int
    from_role: str
    to_role: str
    start_time: Optional[datetime]
    event: Union[CollectionEvent, TransportEvent, ProcessingEvent, QualityTest, ManufacturingEvent, PackingEvent]