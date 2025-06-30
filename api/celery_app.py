"""
Celery application configuration
"""

from celery import Celery
from api.config import settings

# Create Celery instance
celery_app = Celery(
    "rapidapply",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["api.tasks"])

# Celery beat schedule
celery_app.conf.beat_schedule = {
    "cleanup-old-applications": {
        "task": "api.tasks.cleanup.cleanup_old_applications",
        "schedule": 3600.0,  # Every hour
    },
    "update-job-listings": {
        "task": "api.tasks.jobs.update_job_listings",
        "schedule": 1800.0,  # Every 30 minutes
    },
}