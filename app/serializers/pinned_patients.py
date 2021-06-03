from pydantic import BaseModel


class CheckPatientPin(BaseModel):
    clinicianId: int
    patientId: int
    pinUnpinFlag: bool
