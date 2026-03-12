from rest_framework.exceptions import ValidationError
from datetime import date

def validate_user_age_from_token(token_birthdate):
    if not token_birthdate:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")
    try:
        birthdate = date.fromisoformat(token_birthdate)
    except Exception:
        raise ValidationError("Некорректный формат даты рождения.")
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
    return True
