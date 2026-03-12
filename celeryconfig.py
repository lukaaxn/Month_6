from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_email_every_hour': {
        'task': 'celery_tasks.send_simple_email',
        'schedule': crontab(minute=0),  # каждый час
        'args': ['recipient@example.com', 'Hourly Notification', 'Это автоматическое сообщение каждый час.'],
    },
}
