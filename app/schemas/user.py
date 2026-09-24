from pydantic import BaseModel, EmailStr
import uuid
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr

    model_config = {
        "from_attributes": True
    }