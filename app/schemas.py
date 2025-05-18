from pydantic import BaseModel,Field,EmailStr,model_validator
from typing import Literal,Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int = Field(gt=0,description="Must be a positive Integer")
    type: Literal["email", "sms", "in-app"]=Field(description="Must be any one of Email,SMS or in-app",example="email")
    message: str=Field(min_length=1,description="Must not be empty")
    email:Optional[EmailStr]=Field(None,
        description="The recipient's email address (required for email notifications).",
        example="user@example.com",
)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15, description="Phone number with country code")


    @model_validator(mode='after')
    def check_contact_fields(self):
        notif_type=self.type
        email=self.email
        phone=self.phone

        if notif_type=="email" and not email:
            raise ValueError("Email is required for type 'Email'")
        if notif_type=="sms" and not phone:
            raise ValueError("Phone number is required for type 'Phone'")
        return self

class NotificationOut(NotificationCreate):
    id: str
    status: str
    created_at: datetime


