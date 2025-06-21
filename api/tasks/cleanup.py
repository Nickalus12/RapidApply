"""
Cleanup tasks
"""

from api.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task
def cleanup_old_applications():
    """Clean up old application data"""
    logger.info("Running cleanup task")
    # TODO: Implement cleanup logic
    return {"status": "completed"}