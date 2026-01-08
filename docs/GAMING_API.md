# Gaming API Documentation

این مستندات نحوه استفاده از API های مربوط به سیستم gamification (سطح، نشان، امتیاز) را توضیح می‌دهد.

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

## 1. مدیریت سطوح (Levels)

### لیست سطوح

**Endpoint:**
```
GET /api/levels/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "code": "beginner",
      "order": 1,
      "title": "سطح مبتدی",
      "description": "سطح اول برای کاربران تازه‌کار",
      "requiredpoints": 0,
      "icon": "level1.png",
      "company": 1,
      "isactive": true,
      "company_name": "نام شرکت",
      "user_levels_count": 25
    },
    {
      "id": 2,
      "code": "intermediate",
      "order": 2,
      "title": "سطح متوسط",
      "description": "سطح دوم برای کاربران متوسط",
      "requiredpoints": 100,
      "icon": "level2.png",
      "company": 1,
      "isactive": true,
      "company_name": "نام شرکت",
      "user_levels_count": 15
    }
  ]
}
```

**فیلدها:**
- `code`: کد/دسته‌بندی سطح
- `order`: ترتیب سطح (1, 2, 3, ...)
- `requiredpoints`: امتیاز مورد نیاز برای رسیدن به این سطح
- `user_levels_count`: تعداد کاربرانی که به این سطح رسیده‌اند

---

### جزئیات سطح

**Endpoint:**
```
GET /api/levels/{id}/
```

---

### ایجاد سطح جدید

**Endpoint:**
```
POST /api/levels/
```

**Request Body:**
```json
{
  "code": "advanced",
  "order": 3,
  "title": "سطح پیشرفته",
  "description": "سطح سوم برای کاربران پیشرفته",
  "requiredpoints": 500,
  "icon": "level3.png",
  "company": 1,
  "isactive": true
}
```

**نکته:** فیلد `order` باید یکتا باشد (unique).

---

### به‌روزرسانی سطح

**Endpoint:**
```
PUT /api/levels/{id}/
PATCH /api/levels/{id}/
```

---

### حذف سطح

**Endpoint:**
```
DELETE /api/levels/{id}/
```

---

## 2. مدیریت سطوح کاربران (User Levels)

### لیست سطوح کاربران

**Endpoint:**
```
GET /api/user-levels/
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "level": 1,
    "currentpoints": 75,
    "reachedat": "2024-01-01T10:00:00Z",
    "user_name": "نام کاربر",
    "user_mobile": "09123456789",
    "level_details": {
      "id": 1,
      "code": "beginner",
      "order": 1,
      "title": "سطح مبتدی",
      "requiredpoints": 0
    }
  }
]
```

---

### ثبت سطح کاربر

**Endpoint:**
```
POST /api/user-levels/
```

**Request Body:**
```json
{
  "user": 1,
  "level": 1,
  "currentpoints": 75,
  "reachedat": "2024-01-01T10:00:00Z"
}
```

**نکته:** هر کاربر می‌تواند فقط یک بار به یک سطح برسد (unique constraint).

---

## 3. مدیریت نشان‌ها (Badges)

### لیست نشان‌ها

**Endpoint:**
```
GET /api/badges/
```

**Response:**
```json
[
  {
    "id": 1,
    "code": "first_mission",
    "title": "اولین ماموریت",
    "description": "تکمیل اولین ماموریت",
    "icon": "badge1.png",
    "mission": 1,
    "company": 1,
    "isactive": true,
    "company_name": "نام شرکت",
    "mission_title": "ماموریت اول",
    "user_badges_count": 10
  }
]
```

**فیلدها:**
- `code`: کد/دسته‌بندی نشان
- `mission`: ماموریت مرتبط (اگر نشان با تکمیل mission کسب شود)
- `user_badges_count`: تعداد کاربرانی که این نشان را کسب کرده‌اند

---

### ایجاد نشان جدید

**Endpoint:**
```
POST /api/badges/
```

**Request Body:**
```json
{
  "code": "perfect_score",
  "title": "نمره کامل",
  "description": "کسب نمره کامل در یک آزمون",
  "icon": "badge2.png",
  "mission": 1,
  "company": 1,
  "isactive": true
}
```

---

## 4. مدیریت نشان‌های کاربران (User Badges)

### لیست نشان‌های کاربران

**Endpoint:**
```
GET /api/user-badges/
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "badge": 1,
    "earnedat": "2024-01-01T10:00:00Z",
    "user_name": "نام کاربر",
    "user_mobile": "09123456789",
    "badge_details": {
      "id": 1,
      "code": "first_mission",
      "title": "اولین ماموریت",
      "icon": "badge1.png"
    }
  }
]
```

---

### ثبت نشان کاربر

**Endpoint:**
```
POST /api/user-badges/
```

**Request Body:**
```json
{
  "user": 1,
  "badge": 1,
  "earnedat": "2024-01-01T10:00:00Z"
}
```

**نکته:** هر کاربر می‌تواند فقط یک بار یک نشان را کسب کند (unique constraint).

---

## 5. مدیریت امتیازات کاربران (User Points)

### لیست امتیازات

**Endpoint:**
```
GET /api/user-points/
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "totalpoints": 250,
    "lastupdated": "2024-01-01T10:00:00Z",
    "user_name": "نام کاربر",
    "user_mobile": "09123456789"
  }
]
```

---

### ایجاد/به‌روزرسانی امتیاز کاربر

**Endpoint:**
```
POST /api/user-points/
```

**Request Body:**
```json
{
  "user": 1,
  "totalpoints": 250
}
```

**نکته:** هر کاربر فقط یک رکورد امتیاز دارد (OneToOne relationship).

---

### به‌روزرسانی امتیاز

**Endpoint:**
```
PUT /api/user-points/{id}/
PATCH /api/user-points/{id}/
```

**Request Body (PATCH):**
```json
{
  "totalpoints": 300
}
```

---

## 6. مدیریت اکشن‌های کاربران (User Actions)

لاگ تمام اکشن‌هایی که کاربر انجام می‌دهد و امتیاز کسب می‌کند.

### لیست اکشن‌ها

**Endpoint:**
```
GET /api/user-actions/
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "actiontype": "complete_mission",
    "pointsearned": 100,
    "description": "تکمیل ماموریت اول",
    "createdat": "2024-01-01T10:00:00Z",
    "user_name": "نام کاربر",
    "user_mobile": "09123456789"
  },
  {
    "id": 2,
    "user": 1,
    "actiontype": "earn_badge",
    "pointsearned": 50,
    "description": "کسب نشان اولین ماموریت",
    "createdat": "2024-01-01T11:00:00Z",
    "user_name": "نام کاربر",
    "user_mobile": "09123456789"
  }
]
```

**انواع actiontype:**
- `complete_mission`: تکمیل ماموریت
- `pass_exam`: قبولی در آزمون
- `earn_badge`: کسب نشان
- و سایر انواع سفارشی

---

### ثبت اکشن جدید

**Endpoint:**
```
POST /api/user-actions/
```

**Request Body:**
```json
{
  "user": 1,
  "actiontype": "complete_mission",
  "pointsearned": 100,
  "description": "تکمیل ماموریت اول"
}
```

**نکته:** فیلد `createdat` به صورت خودکار تنظیم می‌شود.

---

## مثال استفاده

### دریافت سطح فعلی کاربر

```javascript
// دریافت سطوح کاربر
const response = await fetch('http://localhost:8000/api/user-levels/?user=1', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const userLevels = await response.json();
const currentLevel = userLevels.results[0]; // آخرین سطح
console.log('سطح فعلی:', currentLevel.level_details.title);
console.log('امتیاز فعلی:', currentLevel.currentpoints);
```

### ثبت امتیاز جدید

```javascript
// به‌روزرسانی امتیاز کاربر
const response = await fetch('http://localhost:8000/api/user-points/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user: 1,
    totalpoints: 350
  })
});

const userPoint = await response.json();
console.log('امتیاز به‌روزرسانی شد:', userPoint);
```

### ثبت اکشن و به‌روزرسانی امتیاز

```javascript
// ثبت اکشن
const actionResponse = await fetch('http://localhost:8000/api/user-actions/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user: 1,
    actiontype: 'complete_mission',
    pointsearned: 100,
    description: 'تکمیل ماموریت اول'
  })
});

const action = await actionResponse.json();

// به‌روزرسانی امتیاز کل کاربر
const currentPoints = 250; // از API دریافت کنید
const newPoints = currentPoints + action.pointsearned;

const pointsResponse = await fetch('http://localhost:8000/api/user-points/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user: 1,
    totalpoints: newPoints
  })
});
```

### بررسی سطح بعدی

```javascript
// دریافت امتیاز فعلی کاربر
const pointsResponse = await fetch('http://localhost:8000/api/user-points/?user=1', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const userPoint = pointsResponse.json().results[0];
const currentPoints = userPoint.totalpoints;

// دریافت تمام سطوح
const levelsResponse = await fetch('http://localhost:8000/api/levels/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const levels = levelsResponse.json().results;

// پیدا کردن سطح بعدی
const nextLevel = levels.find(level => 
  level.requiredpoints > currentPoints && level.isactive
);

if (nextLevel) {
  console.log('سطح بعدی:', nextLevel.title);
  console.log('امتیاز مورد نیاز:', nextLevel.requiredpoints);
  console.log('امتیاز باقیمانده:', nextLevel.requiredpoints - currentPoints);
}
```

### دریافت نشان‌های کاربر

```javascript
const response = await fetch('http://localhost:8000/api/user-badges/?user=1', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const userBadges = await response.json();
console.log('نشان‌های کاربر:', userBadges.results.map(ub => ub.badge_details.title));
```

---

## کدهای خطا

- **200 OK**: درخواست موفق
- **201 Created**: ایجاد موفق
- **204 No Content**: حذف موفق
- **400 Bad Request**: 
  - داده‌های ارسالی نامعتبر
  - سطح یا نشان تکراری برای کاربر
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

1. **سطح یکتا:** هر کاربر می‌تواند فقط یک بار به یک سطح برسد.

2. **نشان یکتا:** هر کاربر می‌تواند فقط یک بار یک نشان را کسب کند.

3. **امتیاز یکتا:** هر کاربر فقط یک رکورد امتیاز دارد.

4. **فیلتر بر اساس Company:** کاربران غیر admin فقط داده‌های شرکت خود را می‌بینند.

5. **ثبت خودکار:** پس از تکمیل ماموریت یا قبولی در آزمون، می‌توانید اکشن و امتیاز را به صورت خودکار ثبت کنید.

6. **لاگ اکشن‌ها:** تمام اکشن‌های کاربر در جدول `useraction` ثبت می‌شود تا تاریخچه کاملی داشته باشید.
