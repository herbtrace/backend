from pydantic import BaseModel, Field
import datetime 

class CropResponse(BaseModel):
    species_common_name: str = Field(..., example="Ashwagandha")
    start_time: datetime.datetime
    end_time: datetime.datetime
    latitude: float
    longitude: float