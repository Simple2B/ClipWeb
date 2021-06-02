from typing import Optional
from pydantic.fields import Field
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from app.models import User


User_In_Pydantic = pydantic_model_creator(
    User, exclude_readonly=True, exclude=["activated", "role"], name="UserIn"
)

User_Pydantic = pydantic_model_creator(User, name="User")


class UserExpTimePydantic(BaseModel):
    expiration_date: int = Field(alias="expirationDate")


class Credentials(BaseModel):
    login: str


class UserCreationCredentials(Credentials):
    expiration_date: int
    password: str


class UserUpdateCredentials(Credentials):
    expiration_date: Optional[int]
    activated: Optional[bool]


class ChangePasswordCredentials(BaseModel):
    password: str
