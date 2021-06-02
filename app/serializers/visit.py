from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import Visit

Visit_Pydantic = pydantic_model_creator(Visit)
VisitIn_Pydantic = pydantic_model_creator(Visit, exclude_readonly=True)


class CheckVisit(BaseModel):
    clinicianId = int
    patientId = int
    pinUnpinFlag = bool
