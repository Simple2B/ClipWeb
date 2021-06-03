from typing import List
from pydantic import BaseModel


class CheckPatientPin(BaseModel):
    pinUnpinFlag: bool


class CheckPatientPinResponse(BaseModel):
    pinnedPatients: List[int]
