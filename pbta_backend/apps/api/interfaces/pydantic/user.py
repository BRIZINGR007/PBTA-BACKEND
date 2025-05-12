from pydantic import BaseModel


class IPY_SignUp(BaseModel):
    name: str
    email: str
    password: str
