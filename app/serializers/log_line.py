from app.models import LogLine
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

LogLine_In_Pydantic = pydantic_model_creator(LogLine, exclude_readonly=True)
LogLine_Pydantic = pydantic_model_creator(LogLine)
Logs_Pydantic = pydantic_queryset_creator(LogLine)
