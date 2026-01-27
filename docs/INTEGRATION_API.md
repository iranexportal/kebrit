# Integration API Documentation (Customer ↔ Kebrit)

این مستندات مخصوص **یکپارچه‌سازی سامانه‌های مشتری** با سامانه‌ی Kebrit است.

## مفاهیم

- **مشتری (Customer)**: هر سامانه/مجموعه آموزشی که از API ما استفاده می‌کند. در دیتابیس معادل `Company` است.
- **دانشجو (Student)**: کاربر نهایی مشتری که آزمون را در Kebrit انجام می‌دهد. در دیتابیس به صورت رکورد `User` در همان `Company` ذخیره می‌شود.
- **TOKEN مشتری (Client Token)**: یک توکن **مجزا برای هر مشتری** که باید در **Header** درخواست‌های سرورِ مشتری به API ما ارسال شود.
- **eurl**: یک عدد که بیانگر **شماره آزمون** است. در پیاده‌سازی فعلی، `eurl == evaluation.id` است.
- **launch_id**: یک UUID که در پاسخ `launch` برمی‌گردد و دانشجو با آن وارد صفحه آزمون می‌شود. این UUID مثل «کلید جلسه آزمون» عمل می‌کند.

---

## احراز هویت (Authentication)

### 1) توکن مشتری (Client Token)

برای تمام درخواست‌های این بخش (هم سمت سرور مشتری و هم سمت فرانت دانشجو) باید توکن مشتری در header ارسال شود.

هدر پیشنهادی:

```
X-Client-Token: <CLIENT_TOKEN_UUID>
```

هدر جایگزین (پشتیبانی می‌شود):

```
Authorization: Token <CLIENT_TOKEN_UUID>
```

#### دریافت/ایجاد توکن مشتری

توکن مشتری در مدل `ClientApiToken` نگهداری می‌شود و می‌توانید آن را از طریق پنل Django Admin بسازید:

- مسیر: `admin/` → `Client api tokens` → `Add`
- فیلدها:
  - `company`: مشتری
  - `uuid`: به صورت خودکار ساخته می‌شود (یا می‌توانید دستی ست کنید)
  - `allowed_callback_hosts` (اختیاری): لیست دامنه‌های مجاز برای `callback_url` به صورت `comma-separated`

> **نکته امنیتی**: در صورت نیاز، می‌توانید برای فرانت یک توکن مشتری جدا با سطح دسترسی محدود تعریف کنید.

---

## جریان کلی (Happy Path)

1) مشتری با `eurl` اطلاعات آزمون را می‌گیرد و در سایت خودش نمایش می‌دهد.
2) وقتی دانشجو روی «شروع آزمون» کلیک می‌کند، سرور مشتری endpoint `launch` را صدا می‌زند و `student_uuid` + `mobile` + `eurl` + `callback_url` را می‌فرستد.
3) API در صورت نبود دانشجو، برای همان مشتری یک رکورد دانشجو ایجاد می‌کند و یک `Quiz` می‌سازد (یا اگر آزمون فعال وجود داشته باشد همان را resume می‌کند).
4) API یک `launch_id` برمی‌گرداند و مشتری دانشجو را به `exam_url` منتقل می‌کند.
5) دانشجو در صفحه آزمون، سوالات را با `GET /api/launch/{launch_id}/` دریافت می‌کند و در پایان با `POST /api/launch/{launch_id}/submit/` آزمون را نهایی می‌کند.
6) بعد از پایان، دانشجو به آدرس `callback_url` مشتری برمی‌گردد و نتیجه آزمون در Query String ارسال می‌شود.

---

## Endpointها

### 1) دریافت اطلاعات آزمون (برای صفحه معرفی آزمون مشتری)

- **Endpoint**: `GET /api/integration/exams/{eurl}/`
- **Auth**: نیازمند `X-Client-Token`

**Response (200):**
```json
{
  "eurl": 12,
  "title": "آزمون نمونه",
  "type": 1,
  "accept_score": 60,
  "number_of_question": 20,
  "duration": 30,
  "can_back": true,
  "is_active": true
}
```

**Response (404):**
```json
{ "error": "Evaluation یافت نشد" }
```

---

### 2) ساخت/شروع جلسه آزمون برای دانشجو (Launch)

- **Endpoint**: `POST /api/integration/exams/launch/`
- **Auth**: نیازمند `X-Client-Token`

**Request Body:**
```json
{
  "student_uuid": "stu-uuid-123",
  "mobile": "09123456789",
  "eurl": 12,
  "callback_url": "https://client.example.com/exam/callback"
}
```

**Response (201):**
```json
{
  "launch_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "exam_url": "https://YOUR_EXAM_FRONT_BASE_URL?launch=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "quiz_id": 345,
  "eurl": 12,
  "student": { "uuid": "stu-uuid-123", "mobile": "09123456789" },
  "is_existing_quiz": false
}
```

**نکات مهم:**
- اگر دانشجو قبلاً برای این مشتری وجود نداشته باشد، **ایجاد می‌شود**.
- اگر برای همان دانشجو و همان آزمون یک `Quiz` فعال وجود داشته باشد، همان `Quiz` **resume** می‌شود و `is_existing_quiz=true` برمی‌گردد.

---

### 3) دریافت سوالات و وضعیت آزمون (دانشجو)

- **Endpoint**: `GET /api/launch/{launch_id}/`
- **Auth**: نیازمند توکن مشتری در header

**Response (200):**
```json
{
  "launch_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "quiz_id": 345,
  "eurl": 12,
  "student": { "uuid": "stu-uuid-123", "mobile": "09123456789" },
  "evaluation": {
    "eurl": 12,
    "title": "آزمون نمونه",
    "accept_score": 60,
    "duration": 30,
    "can_back": true,
    "number_of_question": 20
  },
  "state": "started",
  "start_at": "2026-01-21T10:00:00Z",
  "end_at": null,
  "questions": [
    {
      "id": 1,
      "description": "...",
      "type": true,
      "c1": "...",
      "c2": "...",
      "c3": "...",
      "c4": "...",
      "weight": 1.0,
      "can_shuffle": false,
      "current_answer": null,
      "done": null
    }
  ]
}
```

---

### 4) ذخیره پاسخ یک سوال (اختیاری)

- **Endpoint**: `POST /api/launch/{launch_id}/answer/`
- **Auth**: نیازمند توکن مشتری در header

**Request Body:**
```json
{
  "question_id": 1,
  "answer": "2",
  "done": "in_progress"
}
```

**Response (200):**
```json
{ "message": "ذخیره شد" }
```

---

### 5) ارسال نهایی آزمون و محاسبه نتیجه (دانشجو)

- **Endpoint**: `POST /api/launch/{launch_id}/submit/`
- **Auth**: نیازمند توکن مشتری در header

**Request Body:**
```json
{
  "responses": [
    { "question_id": 1, "answer": "2", "done": "completed" },
    { "question_id": 2, "answer": "4", "done": "completed" }
  ]
}
```

**Response (200):**
```json
{
  "message": "پاسخ‌ها ثبت و آزمون پایان یافت",
  "result": {
    "quiz_id": 345,
    "total_questions": 20,
    "correct_answers": 14,
    "wrong_answers": 6,
    "percentage": 70.0,
    "total_score": 14.0,
    "is_accept": true,
    "state": "completed",
    "responses": [
      { "id": 1, "quiz": 345, "question": 1, "answer": "2", "score": 1.0, "done": "completed", "question_details": { /* ... */ } }
    ]
  },
  "redirect_url": "https://client.example.com/exam/callback?student_uuid=stu-uuid-123&mobile=09123456789&eurl=12&quiz_id=345&percentage=70&total_score=14&is_accept=True&state=completed&launch_id=..."
}
```

---

### 6) ریدایرکت مرورگر به callback_url مشتری (دانشجو)

- **Endpoint**: `GET /api/launch/{launch_id}/redirect/`
- **Auth**: نیازمند توکن مشتری در header
- **Behavior**: پاسخ `302` و انتقال مرورگر به `callback_url` با پارامترهای نتیجه

**اگر آزمون تمام نشده باشد:**
```json
{ "error": "آزمون هنوز تمام نشده است" }
```

---

## قرارداد Callback (آنچه مشتری دریافت می‌کند)

پس از پایان آزمون، دانشجو به URL ارسال‌شده توسط مشتری (`callback_url`) برمی‌گردد و این پارامترها اضافه می‌شوند:

- `student_uuid`
- `mobile`
- `eurl`
- `quiz_id`
- `percentage`
- `total_score`
- `is_accept`
- `state`
- `launch_id`

---

## چک‌لیست Front (سایت Kebrit)

- ساخت صفحه آزمون که `launch` را از Query/String بخواند.
- فراخوانی `GET /api/launch/{launch_id}/` برای گرفتن سوالات و نمایش UI آزمون (همراه با `X-Client-Token`).
- ذخیره پاسخ‌ها (یا تدریجی با `/answer/` یا یکجا با `/submit/`) همراه با `X-Client-Token`.
- پس از `submit`:
  - نمایش نتیجه
  - سپس redirect به `redirect_url` یا مستقیماً باز کردن `/api/launch/{launch_id}/redirect/`
- مدیریت خطاهای `404 launch` و `400 submit` (پاسخ ناقص/آزمون تمام شده).

---

## چک‌لیست مشتریان (سیستم‌های مشتری)

- ساخت صفحه معرفی آزمون:
  - دریافت اطلاعات با `GET /api/integration/exams/{eurl}/`
- روی کلیک «شروع آزمون»:
  - فراخوانی `POST /api/integration/exams/launch/` با `student_uuid`, `mobile`, `eurl`, `callback_url` و ارسال توکن مشتری در header
  - ریدایرکت مرورگر دانشجو به `exam_url` و تنظیم توکن مشتری در header درخواست‌های بعدی فرانت
- پیاده‌سازی endpoint/صفحه‌ی `callback_url` برای دریافت نتیجه از Query String و ثبت کارنامه/وضعیت در سیستم مشتری.

