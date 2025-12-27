# Kebrit API - سیستم گیمیفیکیشن

این پروژه یک API بک‌اند برای سیستم گیمیفیکیشن است که با Django و Django REST Framework ساخته شده است. این سیستم چند‌مستاجری (Multi-tenant) است و از `companyId` برای جداسازی داده‌ها استفاده می‌کند.

## 📋 فهرست مطالب

- [پیش‌نیازها](#پیش‌نیازها)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [ساختار پروژه](#ساختار-پروژه)
- [پایگاه داده](#پایگاه-داده)
- [اجرای پروژه](#اجرای-پروژه)
- [API Endpoints](#api-endpoints)
- [احراز هویت (Authentication)](#احراز-هویت)
- [تست‌ها](#تست‌ها)
- [امنیت](#امنیت)

## 🔧 پیش‌نیازها

- Python 3.8 یا بالاتر
- PostgreSQL 12 یا بالاتر
- pip (مدیر بسته Python)
- virtualenv (برای محیط مجازی)

## 📦 نصب و راه‌اندازی

### گام 1: کلون کردن پروژه

```bash
cd /Users/hajrezvan/Desktop/Projects/Kebrit/api
```

### گام 2: ایجاد و فعال‌سازی محیط مجازی

```bash
# ایجاد محیط مجازی
python3 -m venv .env

# فعال‌سازی محیط مجازی
source .env/bin/activate  # برای macOS/Linux
# یا
.env\Scripts\activate  # برای Windows
```

### گام 3: نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### گام 4: تنظیم پایگاه داده PostgreSQL

1. PostgreSQL را نصب و اجرا کنید
2. یک پایگاه داده ایجاد کنید:

```sql
CREATE DATABASE kebrit_db;
```

3. Schema های مورد نیاز را ایجاد کنید:

```sql
CREATE SCHEMA roadmap;
CREATE SCHEMA users;
CREATE SCHEMA exam;
CREATE SCHEMA media;
```

### گام 5: تنظیم فایل settings.py

فایل `kebrit_api/settings.py` را باز کنید و اطلاعات پایگاه داده را تنظیم کنید:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kebrit_db',           # نام پایگاه داده
        'USER': 'postgres',             # نام کاربری PostgreSQL
        'PASSWORD': 'your_password',    # رمز عبور PostgreSQL
        'HOST': 'localhost',           # آدرس هاست
        'PORT': '5432',                 # پورت
        'OPTIONS': {
            'options': '-c search_path=roadmap,users,exam,media,public'
        },
    }
}
```

### گام 6: اجرای Migration ها

```bash
# ایجاد migration ها
python manage.py makemigrations

# اعمال migration ها به پایگاه داده
python manage.py migrate
```

### گام 7: ایجاد کاربر ابری (Superuser) - اختیاری

```bash
python manage.py createsuperuser
```

## 🏗️ ساختار پروژه

```
kebrit_api/
├── kebrit_api/              # تنظیمات اصلی پروژه
│   ├── settings.py         # تنظیمات Django و DRF
│   ├── urls.py             # URL routing اصلی
│   └── ...
├── users_app/              # اپلیکیشن کاربران
│   ├── models.py          # مدل‌های: Company, User, Session, Token, Role, UserRole
│   ├── serializers.py     # Serializer های API
│   ├── views.py           # ViewSet های CRUD
│   ├── permissions.py     # دسترسی‌های سفارشی
│   └── authentication.py  # احراز هویت JWT سفارشی
├── roadmap_app/            # اپلیکیشن نقشه راه
│   ├── models.py          # مدل‌های: Mission, MissionRelation, MissionResult, Ability
│   ├── serializers.py
│   └── views.py
├── exam_app/               # اپلیکیشن آزمون
│   ├── models.py          # مدل‌های: Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation
│   ├── serializers.py
│   └── views.py
├── media_app/              # اپلیکیشن رسانه
│   ├── models.py          # مدل‌های: File, Tag, FileTag
│   ├── serializers.py
│   └── views.py
├── manage.py
└── requirements.txt
```

### توضیح هر بخش:

#### users_app
- **مدیریت کاربران و شرکت‌ها**: شامل مدل‌های Company, User, Role, UserRole
- **مدیریت Session و Token**: برای مدیریت جلسات کاربران
- **احراز هویت**: سیستم JWT برای احراز هویت کاربران

#### roadmap_app
- **مدیریت Mission ها**: ماموریت‌های گیمیفیکیشن
- **روابط Mission ها**: ارتباطات والد-فرزند بین Mission ها
- **نتایج Mission ها**: نتایج و دستاوردهای کاربران
- **Ability ها**: توانایی‌های قابل کسب

#### exam_app
- **Evaluation**: ارزیابی‌ها و آزمون‌ها
- **Question**: سوالات آزمون
- **Quiz**: آزمون‌های انجام شده توسط کاربران
- **QuizResponse**: پاسخ‌های کاربران به سوالات
- **QuizResponseEvaluation**: ارزیابی پاسخ‌ها

#### media_app
- **File**: مدیریت فایل‌ها و رسانه‌ها
- **Tag**: برچسب‌های فایل‌ها
- **FileTag**: ارتباط فایل‌ها و برچسب‌ها

## 🗄️ پایگاه داده

پروژه از PostgreSQL با 4 Schema استفاده می‌کند:

- **users**: داده‌های کاربران، شرکت‌ها، نقش‌ها
- **roadmap**: داده‌های Mission ها و Ability ها
- **exam**: داده‌های آزمون‌ها و سوالات
- **media**: داده‌های فایل‌ها و رسانه‌ها

## 🚀 اجرای پروژه

### اجرای سرور توسعه

```bash
# اطمینان حاصل کنید که محیط مجازی فعال است
source .env/bin/activate

# اجرای سرور
python manage.py runserver
```

سرور روی آدرس `http://127.0.0.1:8000` اجرا می‌شود.

### دسترسی به پنل ادمین

```
http://127.0.0.1:8000/admin/
```

## 📡 API Endpoints

همه endpoint ها با پیشوند `/api/` شروع می‌شوند.

### 🔐 احراز هویت (Authentication)

#### دریافت Token
```http
POST /api/token/
Content-Type: application/json

{
  "username": "user_id",
  "password": "user_password"
}
```

**پاسخ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### تازه‌سازی Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### بررسی اعتبار Token
```http
POST /api/token/verify/
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 👥 Users App Endpoints

#### Companies
```http
GET    /api/companies/              # لیست همه شرکت‌ها
POST   /api/companies/               # ایجاد شرکت جدید
GET    /api/companies/{id}/          # جزئیات یک شرکت
PUT    /api/companies/{id}/          # به‌روزرسانی کامل
PATCH  /api/companies/{id}/          # به‌روزرسانی جزئی
DELETE /api/companies/{id}/          # حذف شرکت
```

**مثال ایجاد شرکت:**
```json
POST /api/companies/
{
  "name": "شرکت نمونه"
}
```

#### Users
```http
GET    /api/users/                   # لیست کاربران
POST   /api/users/                   # ایجاد کاربر جدید
GET    /api/users/{id}/              # جزئیات کاربر
PUT    /api/users/{id}/               # به‌روزرسانی کامل
PATCH  /api/users/{id}/               # به‌روزرسانی جزئی
DELETE /api/users/{id}/               # حذف کاربر
```

**مثال ایجاد کاربر:**
```json
POST /api/users/
{
  "uuid": "user-uuid-123",
  "company": 1,
  "mobile": "09123456789",
  "name": "علی احمدی",
  "password": "secure_password"
}
```

#### Sessions
```http
GET    /api/sessions/
POST   /api/sessions/
GET    /api/sessions/{uuid}/
PUT    /api/sessions/{uuid}/
PATCH  /api/sessions/{uuid}/
DELETE /api/sessions/{uuid}/
```

#### Tokens
```http
GET    /api/tokens/
POST   /api/tokens/
GET    /api/tokens/{uuid}/
PUT    /api/tokens/{uuid}/
PATCH  /api/tokens/{uuid}/
DELETE /api/tokens/{uuid}/
```

#### Roles
```http
GET    /api/roles/
POST   /api/roles/
GET    /api/roles/{id}/
PUT    /api/roles/{id}/
PATCH  /api/roles/{id}/
DELETE /api/roles/{id}/
```

#### User Roles
```http
GET    /api/user-roles/
POST   /api/user-roles/
GET    /api/user-roles/{id}/
PUT    /api/user-roles/{id}/
PATCH  /api/user-roles/{id}/
DELETE /api/user-roles/{id}/
```

### 🗺️ Roadmap App Endpoints

#### Missions
```http
GET    /api/missions/                # لیست Mission ها
POST   /api/missions/                # ایجاد Mission جدید
GET    /api/missions/{id}/           # جزئیات Mission
PUT    /api/missions/{id}/           # به‌روزرسانی کامل
PATCH  /api/missions/{id}/           # به‌روزرسانی جزئی
DELETE /api/missions/{id}/           # حذف Mission
```

**مثال ایجاد Mission:**
```json
POST /api/missions/
{
  "company": 1,
  "user": 1,
  "type": "A",
  "title": "ماموریت نمونه",
  "content": "توضیحات ماموریت",
  "mo": true,
  "point": 100,
  "expier_at": "2024-12-31T23:59:59Z",
  "is_active": true,
  "at_least_point": 50
}
```

#### Mission Relations
```http
GET    /api/mission-relations/
POST   /api/mission-relations/
GET    /api/mission-relations/{id}/
PUT    /api/mission-relations/{id}/
PATCH  /api/mission-relations/{id}/
DELETE /api/mission-relations/{id}/
```

#### Mission Results
```http
GET    /api/mission-results/
POST   /api/mission-results/
GET    /api/mission-results/{id}/
PUT    /api/mission-results/{id}/
PATCH  /api/mission-results/{id}/
DELETE /api/mission-results/{id}/
```

#### Abilities
```http
GET    /api/abilities/
POST   /api/abilities/
GET    /api/abilities/{id}/
PUT    /api/abilities/{id}/
PATCH  /api/abilities/{id}/
DELETE /api/abilities/{id}/
```

### 📝 Exam App Endpoints

#### Evaluations
```http
GET    /api/evaluations/
POST   /api/evaluations/
GET    /api/evaluations/{id}/
PUT    /api/evaluations/{id}/
PATCH  /api/evaluations/{id}/
DELETE /api/evaluations/{id}/
```

**مثال ایجاد Evaluation:**
```json
POST /api/evaluations/
{
  "type": true,
  "accept_score": 70,
  "number_of_question": 10,
  "mission": 1,
  "user": 1,
  "is_active": true,
  "can_back": true,
  "duration": 3600
}
```

#### Questions
```http
GET    /api/questions/
POST   /api/questions/
GET    /api/questions/{id}/
PUT    /api/questions/{id}/
PATCH  /api/questions/{id}/
DELETE /api/questions/{id}/
```

#### Quizzes
```http
GET    /api/quizzes/
POST   /api/quizzes/
GET    /api/quizzes/{id}/
PUT    /api/quizzes/{id}/
PATCH  /api/quizzes/{id}/
DELETE /api/quizzes/{id}/
```

#### Quiz Responses
```http
GET    /api/quiz-responses/
POST   /api/quiz-responses/
GET    /api/quiz-responses/{id}/
PUT    /api/quiz-responses/{id}/
PATCH  /api/quiz-responses/{id}/
DELETE /api/quiz-responses/{id}/
```

#### Quiz Response Evaluations
```http
GET    /api/quiz-response-evaluations/
POST   /api/quiz-response-evaluations/
GET    /api/quiz-response-evaluations/{id}/
PUT    /api/quiz-response-evaluations/{id}/
PATCH  /api/quiz-response-evaluations/{id}/
DELETE /api/quiz-response-evaluations/{id}/
```

### 📁 Media App Endpoints

#### Files
```http
GET    /api/files/
POST   /api/files/
GET    /api/files/{id}/
PUT    /api/files/{id}/
PATCH  /api/files/{id}/
DELETE /api/files/{id}/
```

**مثال ایجاد File:**
```json
POST /api/files/
{
  "user": 1,
  "company": 1,
  "product_id": 123,
  "file_name": "document.pdf",
  "file_type": "application/pdf",
  "file_size": 1024000,
  "path": "/uploads/documents/document.pdf",
  "bucket": "my-bucket",
  "url": "https://example.com/files/document.pdf",
  "is_public": false
}
```

#### Tags
```http
GET    /api/tags/
POST   /api/tags/
GET    /api/tags/{id}/
PUT    /api/tags/{id}/
PATCH  /api/tags/{id}/
DELETE /api/tags/{id}/
```

#### File Tags
```http
GET    /api/file-tags/
POST   /api/file-tags/
GET    /api/file-tags/{id}/
PUT    /api/file-tags/{id}/
PATCH  /api/file-tags/{id}/
DELETE /api/file-tags/{id}/
```

## 🔐 احراز هویت

### استفاده از JWT Token

برای دسترسی به endpoint های محافظت شده، باید Token را در header ارسال کنید:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### مثال کامل با cURL

```bash
# دریافت Token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user_id",
    "password": "password"
  }'

# استفاده از Token برای دسترسی به API
curl -X GET http://127.0.0.1:8000/api/missions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### مثال با Python requests

```python
import requests

# دریافت Token
response = requests.post('http://127.0.0.1:8000/api/token/', json={
    'username': 'user_id',
    'password': 'password'
})
token = response.json()['access']

# استفاده از Token
headers = {'Authorization': f'Bearer {token}'}
missions = requests.get('http://127.0.0.1:8000/api/missions/', headers=headers)
print(missions.json())
```

## 🧪 تست‌ها

### محل فایل‌های تست

فایل‌های تست در هر اپلیکیشن در فایل `tests.py` قرار دارند:

- `users_app/tests.py`
- `roadmap_app/tests.py`
- `exam_app/tests.py`
- `media_app/tests.py`

### اجرای تست‌ها

```bash
# اجرای همه تست‌ها
python manage.py test

# اجرای تست‌های یک اپلیکیشن خاص
python manage.py test users_app
python manage.py test roadmap_app
python manage.py test exam_app
python manage.py test media_app

# اجرای یک تست خاص
python manage.py test users_app.tests.CompanyTestCase
```

### نوشتن تست جدید

مثال تست برای Company:

```python
# users_app/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Company

class CompanyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name="شرکت تست")
    
    def test_list_companies(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_company(self):
        data = {'name': 'شرکت جدید'}
        response = self.client.post('/api/companies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## 🔒 امنیت

### دسترسی‌های چند‌مستاجری

- هر کاربر فقط به داده‌های شرکت خود دسترسی دارد
- کاربران با نقش Admin به همه داده‌ها دسترسی دارند
- فیلتر خودکار بر اساس `companyId` در همه ViewSet ها اعمال می‌شود

### Rate Limiting

- GET requests: 100 درخواست در ساعت
- POST/PUT/PATCH/DELETE: 50 درخواست در ساعت

### CORS

CORS برای دامنه‌های زیر فعال است:
- `http://localhost:3000`
- `http://localhost:8000`

برای اضافه کردن دامنه جدید، فایل `settings.py` را ویرایش کنید:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://your-domain.com",
]
```

## 📊 Pagination

همه endpoint ها از pagination استفاده می‌کنند:
- هر صفحه حداکثر 100 آیتم
- استفاده از query parameter `?page=2` برای صفحه بعدی

## 🐛 عیب‌یابی

### مشکل اتصال به پایگاه داده

```bash
# بررسی اتصال PostgreSQL
psql -U postgres -d kebrit_db

# بررسی migration ها
python manage.py showmigrations
```

### مشکل با Token

- مطمئن شوید که Token را در header ارسال می‌کنید
- بررسی کنید که Token منقضی نشده باشد
- از endpoint `/api/token/refresh/` برای تازه‌سازی استفاده کنید

### مشکل با Permissions

- بررسی کنید که کاربر دارای `companyId` است
- برای دسترسی Admin، مطمئن شوید که کاربر دارای نقش Admin است

## 📝 نکات مهم

1. **مدیریت Migration ها**: اگر schema پایگاه داده از قبل وجود دارد، ممکن است نیاز به تنظیم `managed = False` در Meta کلاس مدل‌ها باشد.

2. **JWT Token**: Token ها به مدت 1 ساعت معتبر هستند. برای تازه‌سازی از endpoint `/api/token/refresh/` استفاده کنید.

3. **CompanyId**: همه درخواست‌ها به صورت خودکار بر اساس `companyId` کاربر فیلتر می‌شوند.

4. **بهینه‌سازی**: از `select_related` برای بهینه‌سازی query ها استفاده شده است.

## 📞 پشتیبانی

برای سوالات و مشکلات، لطفاً issue ایجاد کنید یا با تیم توسعه تماس بگیرید.

## 📄 لایسنس

این پروژه برای استفاده داخلی است.

