CELERY_IMPORTS = ('tasks')
CELERY_IGNORE_RESULT = False
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 5672
BROKER_URL = 'amqp://'

CELERY_RESULT_BACKEND = 'amqp://localhost:5672'

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'reading-file-every-5-second': {
        'task': 'tasks.reading_file',
        'schedule': timedelta(seconds=5)
    }
}
