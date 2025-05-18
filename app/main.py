from fastapi import FastAPI
from app.routes.notification import router as notification_router

app=FastAPI(title="Notification Service",description="It is a notification service application")

app.include_router(notification_router,prefix="/api/v1")
