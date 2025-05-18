from fastapi import APIRouter,HTTPException,Path,BackgroundTasks
from app.schemas import NotificationCreate,NotificationOut
from app.crud import create_notification,get_notificationby_user
from app.db import notifications_collection
from app.tasks.notifier_tasks import send_email_task,send_in_app_task,send_sms_task
router= APIRouter()

@router.get("/",summary="Test the base URL",description="This endpoint simply returns a message to indicate that the base URL is working.")
async def test()->str:
    return "This is the base url. Made by:-Lalatendu Rajguru. A student of CSE in KIIT University"

@router.post("/notifications", response_model=NotificationOut,summary="Send a new notification",
    description="""
    Endpoint to send notifications to users. Supports email, SMS, and in-app notification types.
    The request body should be a JSON object conforming to the NotificationCreate schema.
    The actual sending of email and SMS is handled asynchronously via Celery.""")
async def send_notification_route(notif: NotificationCreate, background_tasks: BackgroundTasks):
    try:
        result = await create_notification(notif)
        notif_id=str(result.id)

        if notif.type == "email":
            send_email_task.delay(notif_id,notif.user_id, notif.message, notif.email)

        elif notif.type == "sms":
            send_sms_task.delay(notif_id, notif.user_id, notif.message,notif.phone)

        elif notif.type == "in-app":
            send_in_app_task.delay(notif_id, notif.user_id, notif.message)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def does_user_exist(user_id:int) -> bool:
    return await notifications_collection.find_one({"user_id": user_id}) is not None

    
@router.get("/users/{user_id}/notifications",response_model=list[NotificationOut],    summary="Get notifications for a specific user",
    description="""
    Retrieves a list of all notification records associated with the given user ID.
    The user_id path parameter must be a positive integer.""")
async def get_user_notifications(user_id:int=Path(...,gt=0,description="Must be a positive integer")):
    try:
        exists=await does_user_exist(user_id)
        if not exists:
            raise HTTPException(status_code=404,detail="User ID not found")
        
        return await get_notificationby_user(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
