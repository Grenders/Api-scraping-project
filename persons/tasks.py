import logging
from celery import shared_task

from persons.models import TaskLog
from persons.scraper import sync_person_api

logger = logging.getLogger(__name__)


@shared_task
def run_sync_with_api() -> None:
    message = "Started syncing with API..."
    logger.info(message)
    TaskLog.objects.create(task_name="Sync API hourly", message=message)

    sync_person_api()

    message = "Finished syncing with API."
    logger.info(message)
    TaskLog.objects.create(task_name="Sync API hourly", message=message)
