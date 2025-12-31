# Kebrit API - سیستم گیمیفیکیشن

این پروژه یک API بک‌اند برای سیستم گیمیفیکیشن است که با Django و Django REST Framework ساخته شده است. این سیستم چند‌مستاجری (Multi-tenant) است و از `companyId` برای جداسازی داده‌ها استفاده می‌کند.

## 📋 فهرست مطالب

- [پیش‌نیازها](#پیش‌نیازها)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [اجرای با Docker](#اجرای-با-docker)
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

### گام 5: تنظیم فایل .env

**⚠️ توجه**: چون دایرکتوری `.env` (محیط مجازی) وجود دارد، باید فایل `.env` را به صورت دستی ایجاد کنید.

1. فایل `.env.example` را باز کنید و محتوای آن را کپی کنید
2. یک فایل جدید با نام `.env` در ریشه پروژه ایجاد کنید (در همان سطح که `manage.py` قرار دارد)
3. محتوای زیر را در فایل `.env` قرار دهید و مقادیر را تغییر دهید:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=kebrit_db
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

**یا با دستور زیر:**

```bash
# در macOS/Linux
cat > .env << 'EOF'
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=kebrit_db
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
EOF
```

**⚠️ مهم**: 
- فایل `.env` حاوی اطلاعات حساس است و نباید در Git commit شود. این فایل به صورت خودکار در `.gitignore` قرار دارد.
- مقادیر `SECRET_KEY` و `DB_PASSWORD` را حتماً تغییر دهید.

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

## 🐳 اجرای با Docker

### پیش‌نیازها برای Docker

- Docker Desktop نصب شده باشد
- Docker Compose در دسترس باشد

### گام 1: تنظیم فایل .env برای Docker

فایل `.env` را ایجاد کنید و تنظیمات زیر را وارد کنید:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
# برای Docker: از 'db' به عنوان host استفاده کنید (نام service در docker-compose)
DB_NAME=kebrit_db
DB_USER=postgres
DB_PASSWORD=your-password-here
DB_HOST=db
DB_PORT=5432
```

**⚠️ مهم**: در Docker، `DB_HOST` باید `db` باشد (نام service در docker-compose.yml)

### گام 2: ساخت و اجرای Container ها

```bash
# ساخت image و اجرای container ها
docker-compose up --build

# یا برای اجرا در background
docker-compose up -d --build
```

### گام 3: اجرای Migration ها (اگر خودکار اجرا نشد)

```bash
# اجرای migration ها
docker-compose exec web python manage.py migrate

# ایجاد superuser
docker-compose exec web python manage.py createsuperuser
```

### دستورات مفید Docker

```bash
# مشاهده لاگ‌ها
docker-compose logs -f

# توقف container ها
docker-compose down

# توقف و حذف volume ها (⚠️ داده‌های پایگاه داده پاک می‌شود)
docker-compose down -v

# اجرای دستورات Django
docker-compose exec web python manage.py <command>

# دسترسی به shell پایگاه داده
docker-compose exec db psql -U postgres -d kebrit_db

# بازسازی image
docker-compose build --no-cache

# مشاهده container های در حال اجرا
docker-compose ps
```

### ساخت Image به صورت جداگانه

اگر می‌خواهید فقط image را بسازید بدون اجرا:

```bash
# ساخت image
docker build -t kebrit-api:latest .

# مشاهده image ساخته شده
docker images | grep kebrit-api
```

### اتصال به پایگاه داده موجود در Docker Compose دیگر

اگر پایگاه داده شما در یک `docker-compose` جداگانه اجرا می‌شود:

1. **ایجاد Network مشترک** (اگر وجود ندارد):

```bash
docker network create kebrit_network
```

2. **اتصال پایگاه داده به Network**:

در `docker-compose.yml` پایگاه داده خود، network را اضافه کنید:

```yaml
services:
  db:
    # ... سایر تنظیمات
    networks:
      - kebrit_network

networks:
  kebrit_network:
    external: true
```

3. **اجرای فقط Django App**:

```bash
# استفاده از docker-compose.web.yml
docker-compose -f docker-compose.web.yml up --build

# یا اگر می‌خواهید فقط service web را از docker-compose اصلی اجرا کنید
docker-compose up web --build
```

4. **تنظیم .env**:

در فایل `.env`، `DB_HOST` را به نام service پایگاه داده در docker-compose دیگر تنظیم کنید:

```env
DB_HOST=db  # یا نام service پایگاه داده شما
```

**نکته**: مطمئن شوید که هر دو container در یک network (`kebrit_network`) هستند.

### دسترسی به API

پس از اجرای Docker Compose، API در آدرس زیر در دسترس است:

```
http://localhost:8000
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

سیستم احراز هویت از **JWT (JSON Web Tokens)** با پشتیبانی از **HttpOnly Cookies** استفاده می‌کند. این سیستم امنیت بالایی را فراهم می‌کند و از ذخیره‌سازی توکن در localStorage جلوگیری می‌کند.

#### ویژگی‌های احراز هویت

- ✅ **JWT Token-based Authentication**: استفاده از Access Token و Refresh Token
- ✅ **HttpOnly Cookies**: توکن‌ها به صورت خودکار در HttpOnly cookies ذخیره می‌شوند
- ✅ **Secure Cookies**: در production، cookies با flag Secure ارسال می‌شوند
- ✅ **Token Blacklisting**: امکان باطل کردن توکن‌ها هنگام logout
- ✅ **Custom Claims**: توکن‌ها شامل `user_id`, `role`, `roles`, `permissions` هستند
- ✅ **Mobile-based Login**: ورود با شماره تلفن به جای username
- ✅ **Permission-based Authorization**: دسترسی بر اساس مجوزها (permissions)

#### دریافت Token (ورود)

```http
POST /api/token/
Content-Type: application/json

{
  "mobile": "09123456789",
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

**نکته**: توکن‌ها به صورت خودکار در HttpOnly cookies نیز ذخیره می‌شوند:
- `access_token`: توکن دسترسی (معمولاً 5 دقیقه)
- `refresh_token`: توکن تازه‌سازی (معمولاً 1 روز)

**JWT Payload شامل:**
```json
{
  "user_id": 1,
  "company_id": 1,
  "name": "علی احمدی",
  "mobile": "09123456789",
  "roles": ["admin", "user"],
  "is_admin": true,
  "permissions": ["admin.read", "admin.write", "admin.delete"]
}
```

#### ورود با API سفارشی

```http
POST /api/login/
Content-Type: application/json

{
  "mobile": "09123456789",
  "password": "user_password"
}
```

**پاسخ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "علی احمدی",
    "mobile": "09123456789",
    "company_id": 1,
    "company_name": "شرکت نمونه"
  }
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

**یا از Cookie:**
```http
POST /api/token/refresh/
```

توکن refresh به صورت خودکار از cookie خوانده می‌شود.

**پاسخ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
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

#### خروج از سیستم (Logout)

```http
POST /api/token/logout/
```

این endpoint توکن refresh را blacklist می‌کند و cookies را پاک می‌کند.

**پاسخ:**
```json
{
  "message": "Successfully logged out"
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

#### ایجاد کاربر جدید با رمز عبور تصادفی

```http
POST /api/users/create/
Content-Type: application/json

{
  "name": "علی احمدی",
  "company_id": 1,
  "uuid": "user-uuid-123",
  "mobile": "09123456789"
}
```

**پاسخ:**
```json
{
  "message": "کاربر با موفقیت ایجاد شد",
  "user_id": 1,
  "mobile": "09123456789",
  "generated_password": "aB3$kL9mN2pQ"
}
```

**نکته**: رمز عبور به صورت خودکار یک رشته 12 کاراکتری تصادفی (شامل حروف، اعداد و کاراکترهای خاص) تولید می‌شود.

#### لیست کاربران یک شرکت

```http
GET /api/users/company/{company_id}/
Authorization: Bearer {access_token}
```

**پاسخ:**
```json
{
  "company_id": 1,
  "company_name": "شرکت نمونه",
  "users": [
    {
      "id": 1,
      "name": "علی احمدی",
      "mobile": "09123456789",
      "uuid": "user-uuid-123",
      "company": 1
    }
  ]
}
```

**نکته**: فقط کاربران همان شرکت یا کاربران Admin می‌توانند لیست کاربران یک شرکت را مشاهده کنند.

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

## 🔐 احراز هویت و مجوزها

### استفاده از JWT Token

سیستم از دو روش برای ارسال توکن پشتیبانی می‌کند:

#### روش 1: HttpOnly Cookies (پیشنهادی)

توکن‌ها به صورت خودکار در HttpOnly cookies ذخیره می‌شوند و در هر درخواست ارسال می‌شوند. این روش امن‌تر است و نیاز به ارسال دستی توکن ندارد.

```python
import requests

# ایجاد session برای نگهداری cookies
session = requests.Session()

# ورود و دریافت توکن (cookies به صورت خودکار ذخیره می‌شوند)
response = session.post('http://127.0.0.1:8000/api/token/', json={
    'mobile': '09123456789',
    'password': 'password'
})

# استفاده از API (cookies به صورت خودکار ارسال می‌شوند)
missions = session.get('http://127.0.0.1:8000/api/missions/')
print(missions.json())
```

#### روش 2: Authorization Header (سازگار با قبل)

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### مثال کامل با cURL

```bash
# دریافت Token (با mobile)
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "09123456789",
    "password": "password"
  }' \
  -c cookies.txt

# استفاده از Token برای دسترسی به API (با cookies)
curl -X GET http://127.0.0.1:8000/api/missions/ \
  -b cookies.txt

# یا با Authorization header
curl -X GET http://127.0.0.1:8000/api/missions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### مثال با Python requests

```python
import requests

# ایجاد session برای نگهداری cookies
session = requests.Session()

# دریافت Token
response = session.post('http://127.0.0.1:8000/api/token/', json={
    'mobile': '09123456789',
    'password': 'password'
})

if response.status_code == 200:
    data = response.json()
    access_token = data['access']
    
    # روش 1: استفاده از cookies (پیشنهادی)
    missions = session.get('http://127.0.0.1:8000/api/missions/')
    print(missions.json())
    
    # روش 2: استفاده از Authorization header
    headers = {'Authorization': f'Bearer {access_token}'}
    missions = requests.get('http://127.0.0.1:8000/api/missions/', headers=headers)
    print(missions.json())
```

### مجوزها و دسترسی‌ها (Authorization)

سیستم از **Permission-based Authorization** استفاده می‌کند. مجوزها در JWT token ذخیره می‌شوند و نیازی به query کردن پایگاه داده در هر درخواست نیست.

#### استفاده از Permission Classes

```python
# در views.py
from users_app.permissions import HasPermission

class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [HasPermission('admin.write')]
    # فقط کاربرانی که مجوز 'admin.write' دارند می‌توانند دسترسی داشته باشند
```

#### مجوزهای پیش‌فرض

- `admin.read`: دسترسی خواندن برای ادمین
- `admin.write`: دسترسی نوشتن برای ادمین
- `admin.delete`: دسترسی حذف برای ادمین

#### بررسی نقش کاربر

```python
# در view یا serializer
if request.user.is_admin:
    # کاربر ادمین است
    pass

if 'admin' in request.user.roles:
    # کاربر دارای نقش admin است
    pass

if 'admin.write' in request.user.permissions:
    # کاربر دارای مجوز admin.write است
    pass
```

### دسترسی‌های چند‌مستاجری

- هر کاربر فقط به داده‌های شرکت خود (`company_id`) دسترسی دارد
- کاربران با نقش **Admin** به همه داده‌ها دسترسی دارند
- فیلتر خودکار بر اساس `company_id` در همه ViewSet ها اعمال می‌شود
- دسترسی به آزمون‌ها محدود به شرکت کاربر است

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
- دسترسی به آزمون‌ها محدود به شرکت کاربر است

### امنیت JWT

- ✅ **HttpOnly Cookies**: جلوگیری از دسترسی JavaScript به توکن‌ها
- ✅ **Secure Cookies**: در production، cookies فقط از طریق HTTPS ارسال می‌شوند
- ✅ **Token Blacklisting**: امکان باطل کردن توکن‌ها هنگام logout
- ✅ **Token Rotation**: تازه‌سازی توکن‌ها برای افزایش امنیت
- ✅ **Short-lived Access Tokens**: توکن‌های دسترسی با عمر کوتاه (5 دقیقه)
- ✅ **Custom Claims**: اطلاعات کاربر در توکن برای کاهش query به پایگاه داده

### Rate Limiting

- GET requests: 100 درخواست در ساعت
- POST/PUT/PATCH/DELETE: 50 درخواست در ساعت
- Login endpoint: 10 درخواست در ساعت
- User creation: 20 درخواست در ساعت

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

**نکته**: برای استفاده از cookies در frontend، باید `credentials: 'include'` را در درخواست‌ها تنظیم کنید:

```javascript
fetch('http://127.0.0.1:8000/api/missions/', {
  credentials: 'include'  // برای ارسال cookies
})
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

2. **JWT Token**: 
   - Access Token به مدت 5 دقیقه معتبر است
   - Refresh Token به مدت 1 روز معتبر است
   - برای تازه‌سازی از endpoint `/api/token/refresh/` استفاده کنید
   - توکن‌ها به صورت خودکار در HttpOnly cookies ذخیره می‌شوند

3. **CompanyId**: همه درخواست‌ها به صورت خودکار بر اساس `companyId` کاربر فیلتر می‌شوند.

4. **بهینه‌سازی**: از `select_related` برای بهینه‌سازی query ها استفاده شده است.

5. **احراز هویت با Mobile**: سیستم از شماره تلفن به جای username برای ورود استفاده می‌کند.

6. **Permission-based Authorization**: برای دسترسی به endpoint های حساس، از `HasPermission` استفاده کنید.

7. **Token Blacklisting**: پس از logout، توکن refresh باطل می‌شود و نمی‌تواند دوباره استفاده شود.

8. **Timezone**: سیستم از timezone `Asia/Tehran` استفاده می‌کند.

## 📞 پشتیبانی

برای سوالات و مشکلات، لطفاً issue ایجاد کنید یا با تیم توسعه تماس بگیرید.

## 📄 لایسنس

این پروژه برای استفاده داخلی است.

