# Python asosida rasm
FROM python:3.10

# Konteyner ichida ishchi katalog yaratish
WORKDIR /app

# Barcha fayllarni konteynerga nusxalash
COPY . /app

# Kutubxonalarni o‘rnatish
RUN pip install --upgrade pip && pip install -r requirements.txt

# Django porti
EXPOSE 8000

# Django serverni ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
