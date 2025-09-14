from fastapi import APIRouter, HTTPException
import json
import datetime
from geopy.geocoders import Nominatim
from models.farmer import CropResponse

router = APIRouter(prefix = "/farmer", tags = ["Farmer"])

def state(latitude,longitude):
    geolocator = Nominatim(user_agent="crop_app")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)

    return location.raw['address']['state']

with open ("validation.json") as f:
        plant_data=json.load(f)

@router.get("/options")
def get_options():

    opt=[
        {"species_common_name": plant["species_common_name"]} for plant in plant_data
    ]
    return opt

@router.post("/validate")
def validate(response : CropResponse):

    plant = next((p for p in plant_data if p["species_common_name"].lower() == response.species_common_name.lower()), None)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found in reference data")

    region = state(response.latitude, response.longitude)
    approved_regions = plant["approved_collection_regions"]
    approved = next((r for r in approved_regions if r['state_name'].lower() == region.lower()), None)
    if not approved:
        raise HTTPException(status_code=400, detail="Region not approved for this crop")
         
    start_month = response.start_time.month
    end_month = response.end_time.month
    if start_month not in plant["allowed_harvest_months"] or end_month not in plant["allowed_harvest_months"] or start_month in plant["restricted_months"] or end_month in plant["restricted_months"]:
        raise HTTPException(status_code=400, detail="Crop not suitable for this season")

    # Blockchain interaction to be added here
    return {
        "species": response.species_common_name,
        "region_valid": True,
        "season_valid": True,
        "message": "Crop cycle validated successfully"
    }

