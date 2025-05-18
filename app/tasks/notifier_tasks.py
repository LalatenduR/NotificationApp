from app.celery_worker import celery_app
from aiosmtplib import SMTP
from email.message import EmailMessage
from dotenv import load_dotenv
from celery import Task
from datetime import datetime, timezone
from pymongo import MongoClient
from bson import ObjectId, errors as bson_errors
import os, asyncio, httpx, traceback

# Load environment variables
load_dotenv()

# Environment setup
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

assert SMTP_HOST and SMTP_PORT and SMTP_USERNAME and SMTP_PASSWORD and FROM_EMAIL, "Missing email configuration environment variables"


client = MongoClient(os.getenv("MONGODB_URL"))
sync_notifications = client.notifications_db.notifications



def update_status(notification_id: str, status: str):
    try:
        object_id = ObjectId(notification_id)
    except bson_errors.InvalidId:
        print(f"Invalid ObjectId: {notification_id}")
        return

    result = sync_notifications.update_one(
        {"_id": object_id},
        {"$set": {"status": status}}
    )



class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 5}
    retry_backoff = True



async def send_email(user_id: int, message: str, to_email: str):
    email = EmailMessage()
    email["From"] = FROM_EMAIL
    email["To"] = to_email
    email["Subject"] = f"Notification for User {user_id}"
    email.set_content(message)

    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True)
    await smtp.connect()
    await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    await smtp.send_message(email)
    await smtp.quit()

    print(f"EMAIL sent to User {user_id} = {to_email}")


@celery_app.task(base=BaseTaskWithRetry, name="send_email_task")
def send_email_task(notification_id: str, user_id: int, message: str, to_email: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_email(user_id, message, to_email))
        update_status(notification_id, "sent")
    except Exception as e:
        traceback.print_exc()
        update_status(notification_id, "failed")
        raise e
    finally:
        loop.close()



async def send_sms(notification_id: str, user_id: int, msg: str, number: str):
    # payload = {
    #     "phone": number,
    #     "message": msg,
    #     "key": "textbelt"
    # }

    # async with httpx.AsyncClient() as client:
    #     res = await client.post("https://textbelt.com/text", data=payload)
    #     result = res.json()
    #     print(f"SMS to User {user_id} = {result}")
    #     if not result.get("success"):
    #         raise Exception("SMS failed")

    print(f"Simulating SMS  sent to {number}")


@celery_app.task(base=BaseTaskWithRetry, name="send_sms_task")
def send_sms_task(notification_id: str, user_id: int, msg: str, number: str):
    try:
        send_sms(notification_id, user_id, msg, number)
        update_status(notification_id, "sent")
    except Exception as e:
        update_status(notification_id, "failed")
        raise e



def send_in_app(user_id: int, message: str):
    print(f"In-App notification to User ID: {user_id}")


@celery_app.task(base=BaseTaskWithRetry, name="send_in_app_task")
def send_in_app_task(notification_id: str, user_id: int, message: str):
    try:
        send_in_app(user_id, message)
        update_status(notification_id, "sent")
    except Exception as e:
        update_status(notification_id, "failed")
        raise e
