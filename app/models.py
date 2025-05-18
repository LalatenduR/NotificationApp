from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Notification(BaseModel):
    id: str
    user_id: int
    type: Literal["email", "sms", "in-app"]
    message: str
    status: str
    created_at: datetime
