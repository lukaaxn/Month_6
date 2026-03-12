from celery import shared_task
import smtplib
from datetime import datetime

# 1. Задача через .delay() — сохранить лог
@shared_task
def save_log(message):
    with open('celery_log.txt', 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")
    return "Log saved"

# 2. Задача по расписанию через crontab — удалить файл
@shared_task
def delete_log_file():
    import os
    try:
        os.remove('celery_log.txt')
        return "Log file deleted"
    except FileNotFoundError:
        return "Log file not found"

# 3. Задача с использованием SMTP — отправить email
@shared_task
def send_simple_email(recipient, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    email_message = f'Subject: {subject}\n\n{message}'
    server.sendmail('your_email@gmail.com', recipient, email_message)
    server.quit()
    return f"Email sent to {recipient}"
