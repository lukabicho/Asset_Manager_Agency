from pydantic import BaseModel, Field, ConfigDict

class AgencyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class AgencyUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class AgencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: int
