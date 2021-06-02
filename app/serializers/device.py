from app.models import Device
from tortoise.contrib.pydantic import pydantic_model_creator

Device_In_Pydantic = pydantic_model_creator(Device, exclude_readonly=True)
Device_Pydantic = pydantic_model_creator(Device)
