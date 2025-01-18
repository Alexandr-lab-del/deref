from django.core.exceptions import ValidationError
import re


def youtube_url_validator(value):
    youtube_pattern = r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$"
    if not re.match(youtube_pattern, value):
        raise ValidationError("Загрузите собственное видео или видео с ютуб")
