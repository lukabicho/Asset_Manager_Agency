import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agency import Agency
from app.schemas.agency import AgencyCreate, AgencyUpdate
from app.core.exceptions import AgencyNotFoundError

class AgencyManager:

    def __init__(self, db: Session):
        self.db = db

    def create_agency(self, *, data: AgencyCreate, owner_id: uuid.UUID):
        agency = Agency(name = data.name, owner_id = owner_id)
        self.db.add(agency)
        self.db.commit()
        self.db.refresh(agency)
        return agency

    def agency_owner_validation(self, agency_id: int, owner_id: uuid.UUID):
        filter_agency = select(Agency).where(Agency.id == agency_id, Agency.owner_id == owner_id)
        query_exec = self.db.scalar(filter_agency)
        if not query_exec:
            raise AgencyNotFoundError("Agency not found")
        return query_exec

    def update_agency(self, *, agency_id: int, data: AgencyUpdate, owner_id:uuid.UUID):
        agency = self.agency_owner_validation(agency_id = agency_id, owner_id = owner_id)
        agency.name = data.name
        self.db.commit()
        self.db.refresh(agency)
        return agency