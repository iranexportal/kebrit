# Kebrit API - راهنمای راه‌اندازی پروژه

این پروژه یک سیستم API برای مدیریت کاربران، ماموریت‌ها، آزمون‌ها، فایل‌ها و سیستم gamification است که با Django و Django REST Framework ساخته شده است.

## پیش‌نیازها

قبل از شروع، مطمئن شوید که موارد زیر روی سیستم شما نصب شده است:

- **Python 3.11+**
- **PostgreSQL 15+**
- **pip** (مدیر بسته Python)
- **Docker و Docker Compose** (اختیاری - برای اجرای با Docker)

## نصب و راه‌اندازی

### روش 1: راه‌اندازی با Docker (پیشنهادی)

1. **کلون کردن پروژه** (اگر از Git استفاده می‌کنید):
```bash
git clone <repository-url>
cd api
```

2. **ایجاد فایل `.env`**:
```bash
cp .env.example .env
```

3. **ویرایش فایل `.env`** و تنظیم مقادیر زیر:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=kebrit_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

4. **اجرای پروژه با Docker Compose**:
```bash
docker-compose up -d
```

این دستور:
- یک container PostgreSQL ایجاد می‌کند
- یک container Django ایجاد می‌کند
- تمام migrations را اجرا می‌کند
- سرور را روی `http://localhost:8000` راه‌اندازی می‌کند

5. **بررسی وضعیت**:
```bash
docker-compose ps
```

6. **مشاهده لاگ‌ها**:
```bash
docker-compose logs -f web
```

### روش 2: راه‌اندازی دستی (بدون Docker)

1. **ایجاد محیط مجازی Python**:
```bash
python3 -m venv venv
source venv/bin/activate  # در Windows: venv\Scripts\activate
```

2. **نصب وابستگی‌ها**:
```bash
pip install -r requirements.txt
```

3. **تنظیم پایگاه داده PostgreSQL**:
   - یک پایگاه داده PostgreSQL ایجاد کنید
   - فایل `.env` را ایجاد و تنظیم کنید:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=kebrit_db
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **ایجاد Schema های پایگاه داده**:
```sql
CREATE SCHEMA IF NOT EXISTS django;
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS roadmap;
CREATE SCHEMA IF NOT EXISTS exam;
CREATE SCHEMA IF NOT EXISTS media;
CREATE SCHEMA IF NOT EXISTS gaming;
```

5. **اجرای Migrations**:
```bash
python manage.py migrate
```

6. **ایجاد کاربر ادمین** (اختیاری):
```bash
python manage.py createsuperuser
```

7. **اجرای سرور**:
```bash
python manage.py runserver
```

سرور روی `http://localhost:8000` در دسترس خواهد بود.

## ساختار پروژه

```
api/
├── kebrit_api/          # تنظیمات اصلی پروژه
│   ├── settings.py      # تنظیمات Django
│   ├── urls.py          # URL routing
│   └── ...
├── users_app/           # مدیریت کاربران و احراز هویت
├── roadmap_app/         # مدیریت ماموریت‌ها و مسیرهای یادگیری
├── exam_app/            # مدیریت آزمون‌ها و سوالات
├── media_app/           # مدیریت فایل‌ها و تگ‌ها
├── gaming_app/          # سیستم gamification (سطح، نشان، امتیاز)
├── requirements.txt     # وابستگی‌های Python
├── docker-compose.yml   # تنظیمات Docker
└── Dockerfile           # تصویر Docker
```

## مستندات API

برای یادگیری نحوه استفاده از API های هر بخش، به فایل‌های مستندات زیر مراجعه کنید:

- **[Users API Documentation](docs/USERS_API.md)** - مدیریت کاربران، احراز هویت و نقش‌ها
- **[Roadmap API Documentation](docs/ROADMAP_API.md)** - مدیریت ماموریت‌ها و مسیرهای یادگیری
- **[Exam API Documentation](docs/EXAM_API.md)** - مدیریت آزمون‌ها، سوالات و پاسخ‌ها
- **[Media API Documentation](docs/MEDIA_API.md)** - مدیریت فایل‌ها و تگ‌ها
- **[Gaming API Documentation](docs/GAMING_API.md)** - سیستم gamification (سطح، نشان، امتیاز)

## احراز هویت

این API از JWT (JSON Web Token) برای احراز هویت استفاده می‌کند.

### دریافت Token

```bash
POST /api/token/
Content-Type: application/json

{
  "mobile": "09123456789",
  "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**پاسخ موفق:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### استفاده از Token

در تمام درخواست‌های بعدی، token را در header ارسال کنید:

```bash
Authorization: Bearer <access_token>
```

### Refresh Token

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Logout

```bash
POST /api/token/logout/
Authorization: Bearer <access_token>
```

## دسترسی به پنل ادمین

پس از راه‌اندازی، می‌توانید به پنل ادمین Django دسترسی داشته باشید:

- **URL**: `http://localhost:8000/admin/`
- از کاربر ادمینی که ایجاد کرده‌اید استفاده کنید

## متغیرهای محیطی

فایل `.env` باید شامل متغیرهای زیر باشد:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Settings
DB_NAME=kebrit_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## دستورات مفید

### اجرای Migrations
```bash
python manage.py migrate
```

### ایجاد Migration جدید
```bash
python manage.py makemigrations
```

### جمع‌آوری فایل‌های Static
```bash
python manage.py collectstatic
```

### اجرای Tests
```bash
python manage.py test
```

### دسترسی به Shell Django
```bash
python manage.py shell
```

### مشاهده لاگ‌های Docker
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### توقف Docker Containers
```bash
docker-compose down
```

### توقف و حذف Volumes
```bash
docker-compose down -v
```

## ساختار پایگاه داده

پروژه از چندین Schema در PostgreSQL استفاده می‌کند:

- **django**: جداول داخلی Django (sessions, migrations, etc.)
- **users**: جداول مربوط به کاربران و شرکت‌ها
- **roadmap**: جداول مربوط به ماموریت‌ها
- **exam**: جداول مربوط به آزمون‌ها
- **media**: جداول مربوط به فایل‌ها
- **gaming**: جداول مربوط به سیستم gamification

## Rate Limiting

API ها دارای محدودیت نرخ درخواست هستند:

- **GET requests**: 100 درخواست در ساعت
- **POST/PUT/PATCH/DELETE**: 50 درخواست در ساعت

## پشتیبانی

برای سوالات و مشکلات، با تیم توسعه تماس بگیرید.

## لایسنس

[لایسنس پروژه را اینجا قرار دهید]
