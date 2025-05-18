from app.db import notifications_collection
from app.schemas import NotificationCreate,NotificationOut
from datetime import datetime,timezone
from typing import List
from app.models import Notification

def mongo_to_pydantic(doc: dict) -> dict:
    doc["id"]=str(doc["_id"])
    del doc["_id"]              
    return doc



async def create_notification(notif: NotificationCreate)->NotificationOut:
    data=notif.model_dump()
    data["status"]="pending"
    data["created_at"]=datetime.now(timezone.utc)
    result=await notifications_collection.insert_one(data)
    data["id"]=str(result.inserted_id)
    return NotificationOut(**data)


async def get_notificationby_user(user_id:int)->List[Notification]:
    notif_cursor=notifications_collection.find({"user_id":user_id})
    notifications=[]
    async for doc in notif_cursor:
        cleaned= mongo_to_pydantic(doc)
        notifications.append(NotificationOut(**cleaned))
    return notifications