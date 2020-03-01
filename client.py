# from celery import Celery
#
# celery = Celery()
# celery.config_from_object('celeryconfig')
#
import time
from tasks import reading_file
while True:
    result = reading_file.delay()
    time.sleep(5)
