"""Agency endpoints module."""
from fastapi import APIRouter, Depends, status

from app.managers.agency_manager import AgencyManager
from app.models.user import User
from app.api.deps import get_agency_manager, get_current_user
from app.schemas.agency import AgencyResponse, AgencyCreate, AgencyUpdate

router = APIRouter(prefix="/agencies", tags=["Agencies"])

@router.post("/", response_model=AgencyResponse, status_code=status.HTTP_201_CREATED)
def create_agency(data: AgencyCreate, agency_manager: AgencyManager = Depends(get_agency_manager), current_user: User = Depends(get_current_user)):
    return agency_manager.create_agency(data=data, owner_id=current_user.id)

@router.patch("/{agency_id}", response_model=AgencyResponse)
def update_agency(agency_id: int, data: AgencyUpdate, agency_manager: AgencyManager = Depends(get_agency_manager), current_user: User = Depends(get_current_user)):
    return agency_manager.update_agency(agency_id=agency_id, data=data, owner_id=current_user.id)