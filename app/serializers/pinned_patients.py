from pydantic import BaseModel


class CheckPatientPin(BaseModel):
    pinUnpinFlag: bool
