# Media API Documentation

این مستندات نحوه استفاده از API های مربوط به مدیریت فایل‌ها و تگ‌ها را توضیح می‌دهد.

## Base URL

```
http://localhost:8000/api
```

## احراز هویت

تمام API های این بخش نیاز به احراز هویت دارند. Token را در header ارسال کنید:

```
Authorization: Bearer <access_token>
```

---

## 1. مدیریت فایل‌ها (Files)

### لیست فایل‌ها

**Endpoint:**
```
GET /api/files/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/files/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "user": 1,
      "company": 1,
      "product_id": null,
      "file_name": "document.pdf",
      "file_type": "application/pdf",
      "file_size": 1024000,
      "path": "/media/files/document.pdf",
      "bucket": "my-bucket",
      "url": "https://example.com/files/document.pdf",
      "is_public": false,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

---

### جزئیات فایل

**Endpoint:**
```
GET /api/files/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "user": 1,
  "company": 1,
  "product_id": null,
  "file_name": "document.pdf",
  "file_type": "application/pdf",
  "file_size": 1024000,
  "path": "/media/files/document.pdf",
  "bucket": "my-bucket",
  "url": "https://example.com/files/document.pdf",
  "is_public": false,
  "created_at": "2024-01-01T10:00:00Z"
}
```

---

### ایجاد فایل جدید

**Endpoint:**
```
POST /api/files/
```

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user": 1,
  "company": 1,
  "product_id": null,
  "file_name": "document.pdf",
  "file_type": "application/pdf",
  "file_size": 1024000,
  "path": "/media/files/document.pdf",
  "bucket": "my-bucket",
  "url": "https://example.com/files/document.pdf",
  "is_public": false
}
```

**فیلدها:**
- `user` (integer, nullable): شناسه کاربر
- `company` (integer, nullable): شناسه شرکت
- `product_id` (integer, nullable): شناسه محصول مرتبط
- `file_name` (string, required): نام فایل
- `file_type` (string, required): نوع فایل (MIME type)
- `file_size` (integer, nullable): اندازه فایل به بایت
- `path` (string, required): مسیر فایل در سرور
- `bucket` (string, nullable): نام bucket (برای cloud storage)
- `url` (string, nullable): URL عمومی فایل
- `is_public` (boolean): آیا فایل عمومی است؟

**Response (201 Created):**
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "user": 1,
  "company": 1,
  "file_name": "document.pdf",
  ...
}
```

**نکته:** فیلد `uuid` به صورت خودکار تولید می‌شود.

---

### به‌روزرسانی فایل

**Endpoint:**
```
PUT /api/files/{id}/
PATCH /api/files/{id}/
```

**Request Body (PATCH):**
```json
{
  "file_name": "new-name.pdf",
  "is_public": true
}
```

---

### حذف فایل

**Endpoint:**
```
DELETE /api/files/{id}/
```

**Response (204 No Content)**

---

## 2. مدیریت تگ‌ها (Tags)

### لیست تگ‌ها

**Endpoint:**
```
GET /api/tags/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "آموزشی"
  },
  {
    "id": 2,
    "title": "ویدیو"
  }
]
```

---

### ایجاد تگ جدید

**Endpoint:**
```
POST /api/tags/
```

**Request Body:**
```json
{
  "title": "مستندات"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "مستندات"
}
```

---

### به‌روزرسانی تگ

**Endpoint:**
```
PUT /api/tags/{id}/
PATCH /api/tags/{id}/
```

---

### حذف تگ

**Endpoint:**
```
DELETE /api/tags/{id}/
```

---

## 3. مدیریت تگ‌های فایل (File Tags)

ارتباط بین فایل‌ها و تگ‌ها.

### لیست تگ‌های فایل

**Endpoint:**
```
GET /api/file-tags/
```

**Response:**
```json
[
  {
    "id": 1,
    "file": 1,
    "tag": 1
  },
  {
    "id": 2,
    "file": 1,
    "tag": 2
  }
]
```

---

### اختصاص تگ به فایل

**Endpoint:**
```
POST /api/file-tags/
```

**Request Body:**
```json
{
  "file": 1,
  "tag": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "file": 1,
  "tag": 1
}
```

---

### حذف تگ از فایل

**Endpoint:**
```
DELETE /api/file-tags/{id}/
```

**Response (204 No Content)**

---

## مثال استفاده

### ایجاد فایل جدید

```javascript
const fileData = {
  user: 1,
  company: 1,
  file_name: 'document.pdf',
  file_type: 'application/pdf',
  file_size: 1024000,
  path: '/media/files/document.pdf',
  bucket: 'my-bucket',
  url: 'https://example.com/files/document.pdf',
  is_public: false
};

const response = await fetch('http://localhost:8000/api/files/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(fileData)
});

const file = await response.json();
console.log('فایل ایجاد شد:', file);
```

### اختصاص تگ به فایل

```javascript
// ابتدا تگ را ایجاد کنید (اگر وجود ندارد)
const tagResponse = await fetch('http://localhost:8000/api/tags/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'آموزشی'
  })
});

const tag = await tagResponse.json();

// سپس تگ را به فایل اختصاص دهید
const fileTagResponse = await fetch('http://localhost:8000/api/file-tags/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    file: 1,
    tag: tag.id
  })
});

const fileTag = await fileTagResponse.json();
console.log('تگ اختصاص داده شد:', fileTag);
```

### دریافت فایل‌های یک کاربر

```javascript
const response = await fetch('http://localhost:8000/api/files/?user=1', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const data = await response.json();
console.log('فایل‌های کاربر:', data.results);
```

---

## کدهای خطا

- **200 OK**: درخواست موفق
- **201 Created**: ایجاد موفق
- **204 No Content**: حذف موفق
- **400 Bad Request**: داده‌های ارسالی نامعتبر
- **401 Unauthorized**: عدم احراز هویت
- **403 Forbidden**: عدم دسترسی
- **404 Not Found**: منبع یافت نشد
- **429 Too Many Requests**: تعداد درخواست‌ها بیش از حد مجاز

---

## Rate Limiting

- **GET requests**: 100 درخواست در ساعت
- **POST/PUT/PATCH/DELETE**: 50 درخواست در ساعت

---

## نکات مهم

1. **UUID خودکار:** هر فایل یک UUID یکتا به صورت خودکار دریافت می‌کند.

2. **فیلتر بر اساس Company:** کاربران غیر admin فقط فایل‌های شرکت خود را می‌بینند.

3. **تگ‌های چندگانه:** یک فایل می‌تواند چندین تگ داشته باشد.

4. **فایل‌های عمومی:** فیلد `is_public` تعیین می‌کند که آیا فایل برای عموم قابل دسترسی است یا خیر.
