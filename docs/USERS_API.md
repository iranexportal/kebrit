# Users API Documentation

این مستندات نحوه استفاده از API های مربوط به مدیریت کاربران، احراز هویت و نقش‌ها را توضیح می‌دهد.

## Base URL

```
http://localhost:8000/api
```

## احراز هویت

تمام API های این بخش نیاز به احراز هویت دارند (به جز endpoint های login و create user).

برای احراز هویت، token را در header درخواست ارسال کنید:

```
Authorization: Bearer <access_token>
```

---

## 1. دریافت Token (ورود)

برای دریافت JWT token بدون نیاز به رمز عبور (با استفاده از token سازمان/مشتری).

**Endpoint:**
```
POST /api/token/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "mobile": "09123456789",
  "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (400 Bad Request):**
```json
{
  "mobile": ["این فیلد الزامی است."],
  "token": ["این فیلد الزامی است."]
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "شماره تلفن یا توکن اشتباه است"
}
```

---

## 2. Refresh Token

برای تازه‌سازی access token.

**Endpoint:**
```
POST /api/token/refresh/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 3. Logout

برای خروج از سیستم و باطل کردن token.

**Endpoint:**
```
POST /api/token/logout/
```

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (اختیاری):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## 4. ایجاد کاربر جدید

ایجاد کاربر جدید (بدون رمز عبور) و صدور توکن (بدون نیاز به احراز هویت).

**Endpoint:**
```
POST /api/users/create/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "نام کاربر",
  "company_id": 1,
  "uuid": "شناسه-یکتای-درون-سازمانی",
  "mobile": "09123456789"
}
```

**Response (201 Created):**
```json
{
  "message": "کاربر با موفقیت ایجاد شد",
  "user_id": 1,
  "name": "نام کاربر",
  "mobile": "09123456789",
  "company": "نام شرکت",
  "token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**نکته:** توکن به صورت خودکار تولید می‌شود و فقط یک بار در پاسخ برگردانده می‌شود.

---

## 5. لیست کاربران

دریافت لیست تمام کاربران (فیلتر شده بر اساس company برای کاربران غیر admin).

**Endpoint:**
```
GET /api/users/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: شماره صفحه (پیش‌فرض: 1)
- `page_size`: تعداد آیتم در هر صفحه (پیش‌فرض: 100)

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "uuid": "uuid-123",
      "company": 1,
      "mobile": "09123456789",
      "name": "نام کاربر"
    }
  ]
}
```

---

## 6. جزئیات کاربر

دریافت اطلاعات یک کاربر خاص.

**Endpoint:**
```
GET /api/users/{id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "uuid": "uuid-123",
  "company": 1,
  "mobile": "09123456789",
  "name": "نام کاربر"
}
```

---

## 7. به‌روزرسانی کاربر

**Endpoint:**
```
PUT /api/users/{id}/
PATCH /api/users/{id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PUT - تمام فیلدها):**
```json
{
  "name": "نام جدید",
  "mobile": "09123456789",
  "company": 1,
  "uuid": "uuid-123"
}
```

**Request Body (PATCH - فقط فیلدهای مورد نظر):**
```json
{
  "name": "نام جدید"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "نام جدید",
  "mobile": "09123456789",
  "company": 1,
  "uuid": "uuid-123"
}
```

---

## 8. حذف کاربر

**Endpoint:**
```
DELETE /api/users/{id}/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content)**

---

## 9. مدیریت شرکت‌ها

### لیست شرکت‌ها
```
GET /api/companies/
```

### جزئیات شرکت
```
GET /api/companies/{id}/
```

### ایجاد شرکت (فقط Admin)
```
POST /api/companies/
```

**Request Body:**
```json
{
  "name": "نام شرکت"
}
```

### به‌روزرسانی شرکت (فقط Admin)
```
PUT /api/companies/{id}/
PATCH /api/companies/{id}/
```

### حذف شرکت (فقط Admin)
```
DELETE /api/companies/{id}/
```

---

## 10. مدیریت نقش‌ها (Roles)

### لیست نقش‌ها
```
GET /api/roles/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "admin",
    "company": 1
  },
  {
    "id": 2,
    "title": "student",
    "company": 1
  }
]
```

### ایجاد نقش
```
POST /api/roles/
```

**Request Body:**
```json
{
  "title": "teacher",
  "company": 1
}
```

---

## 11. مدیریت نقش‌های کاربر (User Roles)

### لیست نقش‌های کاربر
```
GET /api/user-roles/
```

### اختصاص نقش به کاربر
```
POST /api/user-roles/
```

**Request Body:**
```json
{
  "user": 1,
  "role": 2
}
```

### حذف نقش از کاربر
```
DELETE /api/user-roles/{id}/
```

---

## 12. مدیریت Session ها

### لیست Session ها
```
GET /api/sessions/
```

### جزئیات Session
```
GET /api/sessions/{uuid}/
```

### حذف Session
```
DELETE /api/sessions/{uuid}/
```

---

## 13. مدیریت Token ها

### لیست Token ها
```
GET /api/tokens/
```

### جزئیات Token
```
GET /api/tokens/{uuid}/
```

### حذف Token
```
DELETE /api/tokens/{uuid}/
```

---

## کدهای خطا

- **200 OK**: درخواست موفق
- **201 Created**: ایجاد موفق
- **204 No Content**: حذف موفق
- **400 Bad Request**: داده‌های ارسالی نامعتبر
- **401 Unauthorized**: عدم احراز هویت یا token نامعتبر
- **403 Forbidden**: عدم دسترسی (مثلاً کاربر غیر admin)
- **404 Not Found**: منبع یافت نشد
- **429 Too Many Requests**: تعداد درخواست‌ها بیش از حد مجاز

---

## Rate Limiting

- **GET requests**: 100 درخواست در ساعت
- **POST/PUT/PATCH/DELETE**: 50 درخواست در ساعت

---

## مثال استفاده در JavaScript (Fetch)

```javascript
// دریافت Token
const response = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    mobile: '09123456789',
    token: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
  })
});

const data = await response.json();
const accessToken = data.access;

// استفاده از Token در درخواست‌های بعدی
const usersResponse = await fetch('http://localhost:8000/api/users/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const users = await usersResponse.json();
```

---

## مثال استفاده در Axios

```javascript
import axios from 'axios';

// تنظیم base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// دریافت Token
const loginResponse = await api.post('/token/', {
  mobile: '09123456789',
  token: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
});

const accessToken = loginResponse.data.access;

// تنظیم token در header برای تمام درخواست‌های بعدی
api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

// دریافت لیست کاربران
const usersResponse = await api.get('/users/');
console.log(usersResponse.data);
```
