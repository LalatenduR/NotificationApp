from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")

celery_app=Celery("worker", broker=CELERY_BROKER_URL)

from app.tasks import notifier_tasks

if __name__ == "__main__":
    celery_app.start()