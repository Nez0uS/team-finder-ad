import io
import random
import re

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


AVATAR_SIZE = 100
AVATAR_FONT_SIZE = 50
AVATAR_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
AVATAR_TEXT_COLOR = 'white'


def validate_phone_number(phone):
    """Валидация и нормализация номера телефона."""
    if not phone:
        return phone
    phone_pattern = re.compile(r'^(\+7|8)\d{10}$')
    if not phone_pattern.match(phone):
        raise ValidationError(
            'Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
        )
    normalized = '+7' + phone[-10:] if phone.startswith('8') else phone
    return normalized


def generate_avatar(user):
    """Генерирует аватар для пользователя на основе первой буквы имени."""
    color = random.choice(AVATAR_COLORS)
    img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color=color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", AVATAR_FONT_SIZE
        )
    except Exception:
        font = ImageFont.load_default()
    char = user.name[0].upper() if user.name else '?'
    bbox = draw.textbbox((0, 0), char, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(
        ((AVATAR_SIZE - w) // 2, (AVATAR_SIZE - h) // 2),
        char, fill=AVATAR_TEXT_COLOR, font=font
    )
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(
        buffer.getvalue(), name=f'avatar_{user.email}.png'
    )
