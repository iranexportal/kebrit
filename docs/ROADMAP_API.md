# Roadmap API Documentation

این مستندات نحوه استفاده از API های مربوط به مدیریت ماموریت‌ها، مسیرهای یادگیری و نتایج ماموریت‌ها را توضیح می‌دهد.

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

## 1. مدیریت ماموریت‌ها (Missions)

### لیست ماموریت‌ها

**Endpoint:**
```
GET /api/missions/
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
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "company": 1,
      "user": null,
      "typeid": 12,
      "typetitle": "تولید محتوا",
      "title": "ماموریت اول",
      "content": "توضیحات ماموریت...",
      "mo": true,
      "point": 100,
      "create_at": "2024-01-01T10:00:00Z",
      "modified_at": null,
      "expier_at": null,
      "is_active": true,
      "at_least_point": 50,
      "ctatext": "شروع",
      "eurl": "1",
      "evaluation_results": [
        {
          "evaluation_id": 1,
          "evaluation_title": "آزمون ماموریت اول",
          "evaluation_type": "quiz",
          "quiz_id": 5,
          "score": 85.5,
          "quiz_start_at": "2024-01-01T10:00:00Z",
          "quiz_end_at": "2024-01-01T10:30:00Z",
          "is_accept": true,
          "accept_score": 50
        }
      ]
    }
  ]
}
```

**نکته:** فیلد `evaluation_results` شامل نتایج آزمون‌های مرتبط با این ماموریت برای کاربر فعلی است.

---

### ساختار شیء ماموریت (خروجی API)

هر جا در این مستندات یک شیء `mission` برگردانده می‌شود، ساختار آن به‌صورت زیر است:

- `id` (integer): شناسه ماموریت
- `company` (integer|null): شناسه شرکت
- `user` (integer|null): شناسه کاربری که ماموریت را تعریف کرده است
- `typeid` (integer|null): شناسه نوع ماموریت (`missiontype.id`)
- `typetitle` (string|null): عنوان نوع ماموریت
- `title` (string): عنوان ماموریت
- `content` (string): توضیحات کامل ماموریت
- `mo` (boolean): آیا ماموریت اجباری است؟
- `point` (integer): امتیاز این ماموریت
- `create_at` (datetime): زمان ایجاد
- `modified_at` (datetime|null): زمان آخرین ویرایش
- `expier_at` (datetime|null): زمان انقضای ماموریت
- `is_active` (boolean): وضعیت فعال/غیرفعال
- `at_least_point` (integer|null): حداقل امتیاز مورد نیاز
- `ctatext` (string|null): متن دکمه «دعوت به اقدام» برای این مأموریت
- `eurl` (string|null): شناسه یکتای آزمون متناظر با این مأموریت (از جدول `evaluation`)
- `evaluation_results` (array): نتایج آزمون‌های مرتبط برای کاربر فعلی (در صورت احراز هویت)

### جزئیات ماموریت

**Endpoint:**
```
GET /api/missions/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "company": 1,
  "user": null,
  "typeid": 12,
  "typetitle": "تولید محتوا",
  "title": "ماموریت اول",
  "content": "توضیحات کامل ماموریت...",
  "mo": true,
  "point": 100,
  "create_at": "2024-01-01T10:00:00Z",
  "modified_at": null,
  "expier_at": null,
  "is_active": true,
  "at_least_point": 50,
  "ctatext": "شروع",
  "eurl": "1",
  "evaluation_results": [
    {
      "evaluation_id": 1,
      "evaluation_title": "آزمون ماموریت اول",
      "evaluation_type": "quiz",
      "quiz_id": 5,
      "score": 85.5,
      "quiz_start_at": "2024-01-01T10:00:00Z",
      "quiz_end_at": "2024-01-01T10:30:00Z",
      "is_accept": true,
      "accept_score": 50
    }
  ]
}
```

---

### ایجاد ماموریت جدید

**Endpoint:**
```
POST /api/missions/
```

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "company": 1,
  "user": null,
  "title": "ماموریت جدید",
  "content": "توضیحات ماموریت",
  "mo": true,
  "point": 100,
  "expier_at": "2024-12-31T23:59:59Z",
  "is_active": true,
  "at_least_point": 50
}
```

**فیلدها:**
- `company` (integer, required): شناسه شرکت
- `user` (integer, nullable): شناسه کاربر (اختیاری)
- `title` (string, required): عنوان ماموریت
- `content` (text, required): محتوای ماموریت
- `mo` (boolean, required): آیا ماموریت اجباری است؟
- `point` (integer, required): امتیاز ماموریت
- `expier_at` (datetime, nullable): تاریخ انقضا
- `is_active` (boolean): آیا ماموریت فعال است؟
- `at_least_point` (integer, nullable): حداقل امتیاز مورد نیاز

**Response (201 Created):**
```json
{
  "id": 1,
  "company": 1,
  "user": null,
  "typeid": 12,
  "typetitle": "تولید محتوا",
  "title": "ماموریت جدید",
  "content": "توضیحات ماموریت",
  "mo": true,
  "point": 100,
  "create_at": "2024-01-01T10:00:00Z",
  "modified_at": null,
  "expier_at": "2024-12-31T23:59:59Z",
  "is_active": true,
  "at_least_point": 50,
  "ctatext": "شروع",
  "eurl": "1",
  "evaluation_results": []
}
```

---

### به‌روزرسانی ماموریت

**Endpoint:**
```
PUT /api/missions/{id}/
PATCH /api/missions/{id}/
```

**Request Body (PATCH):**
```json
{
  "title": "عنوان جدید",
  "is_active": false
}
```

---

### حذف ماموریت

**Endpoint:**
```
DELETE /api/missions/{id}/
```

**Response (204 No Content)**

---

## 2. دریافت ماموریت‌های کاربر

این endpoint ماموریت‌های انجام شده و در دسترس کاربر را برمی‌گرداند.

**Endpoint:**
```
POST /api/user-missions/
```

**Headers:**
```
Content-Type: application/json
```

**نکته:** این endpoint نیاز به احراز هویت ندارد.

**Request Body:**
```json
{
  "mobile": "09123456789",
  "company_id": 1
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "name": "نام کاربر",
    "mobile": "09123456789",
    "company_id": 1,
    "company_name": "نام شرکت"
  },
  "completed_missions": [
    {
      "mission": {
        "id": 1,
        "company": 1,
        "user": 1,
        "typeid": 12,
        "typetitle": "تولید محتوا",
        "title": "ماموریت اول",
        "content": "...",
        "mo": true,
        "point": 100,
        "create_at": "2024-01-01T10:00:00Z",
        "modified_at": null,
        "expier_at": null,
        "is_active": true,
        "at_least_point": 50,
        "ctatext": "شروع",
        "eurl": "1",
        "evaluation_results": []
      },
      "result": {
        "id": 1,
        "mission": 1,
        "user": 1,
        "state": "completed",
        "user_grant": null,
        "quiz_id": 5,
        "ability": null
      }
    }
  ],
  "available_missions": [
    {
      "id": 2,
      "company": 1,
      "user": 1,
      "typeid": 13,
      "typetitle": "مشاهده ویدیو",
      "title": "ماموریت دوم",
      "content": "...",
      "mo": false,
      "point": 150,
      "create_at": "2024-01-02T10:00:00Z",
      "modified_at": null,
      "expier_at": null,
      "is_active": true,
      "at_least_point": null,
      "ctatext": "مشاهده",
      "eurl": "2",
      "evaluation_results": []
    }
  ],
  "stats": {
    "total_completed": 1,
    "total_available": 5
  }
}
```

---

## 3. مدیریت روابط ماموریت‌ها (Mission Relations)

روابط بین ماموریت‌ها (والد-فرزند) را مدیریت می‌کند.

### لیست روابط

**Endpoint:**
```
GET /api/mission-relations/
```

**Response:**
```json
[
  {
    "id": 1,
    "mission": 1,
    "parent": null,
    "child": 2
  }
]
```

### ایجاد رابطه جدید

**Endpoint:**
```
POST /api/mission-relations/
```

**Request Body:**
```json
{
  "mission": 1,
  "parent": null,
  "child": 2
}
```

---

## 4. مدیریت نتایج ماموریت‌ها (Mission Results)

نتایج انجام ماموریت‌ها توسط کاربران.

### لیست نتایج

**Endpoint:**
```
GET /api/mission-results/
```

**Response:**
```json
[
  {
    "id": 1,
    "mission": 1,
    "user": 1,
    "state": "completed",
    "user_grant": null,
    "quiz_id": 5,
    "ability": null
  }
]
```

### ایجاد نتیجه جدید

**Endpoint:**
```
POST /api/mission-results/
```

**Request Body:**
```json
{
  "mission": 1,
  "user": 1,
  "state": "completed",
  "quiz_id": 5,
  "ability": null
}
```

**فیلد `state` می‌تواند مقادیر زیر را داشته باشد:**
- `"completed"`: تکمیل شده
- `"in_progress"`: در حال انجام
- `"pending"`: در انتظار
- و سایر مقادیر سفارشی

---

## 5. مدیریت توانایی‌ها (Abilities)

### لیست توانایی‌ها

**Endpoint:**
```
GET /api/abilities/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "برنامه‌نویسی Python",
    "company": 1
  }
]
```

### ایجاد توانایی جدید

**Endpoint:**
```
POST /api/abilities/
```

**Request Body:**
```json
{
  "title": "برنامه‌نویسی JavaScript",
  "company": 1
}
```

---

## مثال استفاده

### دریافت ماموریت‌های کاربر

```javascript
const response = await fetch('http://localhost:8000/api/user-missions/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    mobile: '09123456789',
    company_id: 1
  })
});

const data = await response.json();
console.log('ماموریت‌های انجام شده:', data.completed_missions);
console.log('ماموریت‌های در دسترس:', data.available_missions);
```

### ایجاد ماموریت جدید

```javascript
const response = await fetch('http://localhost:8000/api/missions/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    company: 1,
    type: 'A',
    title: 'ماموریت جدید',
    content: 'توضیحات ماموریت',
    mo: true,
    point: 100,
    is_active: true
  })
});

const mission = await response.json();
console.log('ماموریت ایجاد شد:', mission);
```

### ثبت نتیجه ماموریت

```javascript
const response = await fetch('http://localhost:8000/api/mission-results/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    mission: 1,
    user: 1,
    state: 'completed',
    quiz_id: 5
  })
});

const result = await response.json();
console.log('نتیجه ثبت شد:', result);
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
