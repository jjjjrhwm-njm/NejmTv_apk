FROM python:3.10-slim

WORKDIR /app

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir aiogram aiohttp

# نسخ الكود
COPY bot_api.py .

# تشغيل السيرفر
CMD ["python", "bot_api.py"]
