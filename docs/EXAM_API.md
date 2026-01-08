# Exam API Documentation

این مستندات نحوه استفاده از API های مربوط به مدیریت آزمون‌ها، سوالات، کوئیزها و پاسخ‌ها را توضیح می‌دهد.

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

## 1. مدیریت نوع ارزیابی (Evaluation Types)

### لیست انواع ارزیابی

**Endpoint:**
```
GET /api/evaluation-types/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "آزمون کوتاه"
  },
  {
    "id": 2,
    "title": "آزمون جامع"
  }
]
```

---

## 2. مدیریت ارزیابی‌ها (Evaluations)

### لیست ارزیابی‌ها

**Endpoint:**
```
GET /api/evaluations/
```

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "آزمون ماموریت اول",
      "type": 1,
      "accept_score": 50,
      "number_of_question": 10,
      "mission": 1,
      "user": 1,
      "create_at": "2024-01-01T10:00:00Z",
      "is_active": true,
      "can_back": true,
      "duration": 30,
      "questions_count": 10,
      "last_score": 85.5,
      "last_quiz_id": 5,
      "type_details": {
        "id": 1,
        "title": "آزمون کوتاه"
      }
    }
  ]
}
```

**فیلدهای اضافی:**
- `questions_count`: تعداد سوالات موجود در بانک سوالات
- `last_score`: نمره آخرین آزمون کاربر (درصد)
- `last_quiz_id`: شناسه آخرین کوئیز کاربر

---

### جزئیات ارزیابی

**Endpoint:**
```
GET /api/evaluations/{id}/
```

---

### دریافت سوالات یک ارزیابی

**Endpoint:**
```
GET /api/evaluations/{id}/questions/
```

**نکته:** این endpoint تمام سوالات را با پاسخ صحیح برمی‌گرداند (برای مدرسان).

**Response:**
```json
{
  "evaluation_id": 1,
  "evaluation_details": {...},
  "total_questions": 10,
  "questions": [
    {
      "id": 1,
      "evaluation": 1,
      "description": "سوال اول؟",
      "img": null,
      "type": true,
      "c1": "گزینه 1",
      "c2": "گزینه 2",
      "c3": "گزینه 3",
      "c4": "گزینه 4",
      "correct": 2,
      "answer": "توضیحات پاسخ",
      "weight": 1.0,
      "can_shuffle": false
    }
  ]
}
```

---

### ایجاد ارزیابی جدید

**Endpoint:**
```
POST /api/evaluations/
```

**Request Body:**
```json
{
  "title": "آزمون جدید",
  "type": 1,
  "accept_score": 50,
  "number_of_question": 10,
  "mission": 1,
  "user": 1,
  "is_active": true,
  "can_back": true,
  "duration": 30
}
```

---

## 3. مدیریت سوالات (Questions)

### لیست سوالات

**Endpoint:**
```
GET /api/questions/
```

**Response:**
```json
[
  {
    "id": 1,
    "evaluation": 1,
    "description": "سوال اول؟",
    "img": null,
    "type": true,
    "c1": "گزینه 1",
    "c2": "گزینه 2",
    "c3": "گزینه 3",
    "c4": "گزینه 4",
    "correct": 2,
    "answer": "توضیحات پاسخ",
    "weight": 1.0,
    "can_shuffle": false
  }
]
```

**نکته:** فیلد `correct` فقط برای مدرسان نمایش داده می‌شود.

---

### ایجاد سوال جدید

**Endpoint:**
```
POST /api/questions/
```

**Request Body:**
```json
{
  "evaluation": 1,
  "description": "سوال جدید؟",
  "img": null,
  "type": true,
  "c1": "گزینه 1",
  "c2": "گزینه 2",
  "c3": "گزینه 3",
  "c4": "گزینه 4",
  "correct": 2,
  "answer": "توضیحات پاسخ",
  "weight": 1.0,
  "can_shuffle": false
}
```

**فیلدها:**
- `type`: `true` برای چندگزینه‌ای، `false` برای تشریحی
- `correct`: شماره گزینه صحیح (1-4) برای سوالات چندگزینه‌ای
- `weight`: وزن سوال در محاسبه نمره

---

## 4. مدیریت کوئیزها (Quizzes)

### لیست کوئیزها

**Endpoint:**
```
GET /api/quizzes/
```

**Response:**
```json
[
  {
    "id": 1,
    "evaluation": 1,
    "user": 1,
    "start_at": "2024-01-01T10:00:00Z",
    "end_at": null,
    "score": null,
    "is_accept": null,
    "state": "started",
    "evaluation_details": {...},
    "questions": [...],
    "responses_count": 0
  }
]
```

---

### شروع کوئیز جدید

**Endpoint:**
```
POST /api/quizzes/start/
```

**Request Body:**
```json
{
  "evaluation_id": 1
}
```

**Response (201 Created):**
```json
{
  "quiz": {
    "id": 1,
    "evaluation": 1,
    "user": 1,
    "start_at": "2024-01-01T10:00:00Z",
    "state": "started",
    ...
  },
  "questions": [
    {
      "id": 1,
      "description": "سوال اول؟",
      "type": true,
      "c1": "گزینه 1",
      "c2": "گزینه 2",
      "c3": "گزینه 3",
      "c4": "گزینه 4",
      "weight": 1.0,
      "can_shuffle": false
    }
  ],
  "message": "کوئیز با موفقیت ایجاد شد"
}
```

**نکته:** 
- سوالات به صورت تصادفی از بانک سوالات انتخاب می‌شوند
- پاسخ صحیح (`correct`) در سوالات نمایش داده نمی‌شود
- اگر کوئیز فعال دیگری برای این evaluation وجود داشته باشد، خطا برمی‌گرداند

---

### دریافت سوالات کوئیز فعال

**Endpoint:**
```
GET /api/quizzes/{id}/questions/
```

**Response:**
```json
{
  "quiz_id": 1,
  "evaluation_id": 1,
  "start_at": "2024-01-01T10:00:00Z",
  "end_at": null,
  "state": "started",
  "questions": [
    {
      "id": 1,
      "description": "سوال اول؟",
      "type": true,
      "c1": "گزینه 1",
      "c2": "گزینه 2",
      "c3": "گزینه 3",
      "c4": "گزینه 4",
      "current_answer": null,
      "done": null
    }
  ]
}
```

**نکته:** `current_answer` پاسخ فعلی کاربر را نشان می‌دهد (اگر قبلاً پاسخ داده باشد).

---

### ارسال پاسخ‌های کوئیز

**Endpoint:**
```
POST /api/quizzes/submit/
```

**Request Body:**
```json
{
  "quiz_id": 1,
  "responses": [
    {
      "question_id": 1,
      "answer": 2,
      "done": "completed"
    },
    {
      "question_id": 2,
      "answer": 1,
      "done": "completed"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "message": "پاسخ‌های کوئیز با موفقیت ثبت شد",
  "result": {
    "quiz_id": 1,
    "total_questions": 10,
    "correct_answers": 8,
    "wrong_answers": 2,
    "percentage": 80.0,
    "total_score": 8.0,
    "is_accept": true,
    "accept_score": 50,
    "responses": [
      {
        "id": 1,
        "quiz": 1,
        "question": 1,
        "answer": 2,
        "score": 1.0,
        "done": "completed",
        "question_details": {...}
      }
    ]
  }
}
```

**نکته:** 
- پس از ارسال پاسخ‌ها، نمره به صورت خودکار محاسبه می‌شود
- اگر کاربر در آزمون قبول شده باشد (`is_accept: true`) و ماموریت مرتبطی وجود داشته باشد، `MissionResult` به صورت خودکار ثبت می‌شود

---

### دریافت نتیجه کوئیز

**Endpoint:**
```
GET /api/quizzes/{id}/result/
```

**Response:**
```json
{
  "quiz_id": 1,
  "total_questions": 10,
  "correct_answers": 8,
  "wrong_answers": 2,
  "percentage": 80.0,
  "total_score": 8.0,
  "is_accept": true,
  "accept_score": 50,
  "start_at": "2024-01-01T10:00:00Z",
  "end_at": "2024-01-01T10:30:00Z",
  "responses": [...]
}
```

---

## 5. مدیریت پاسخ‌های کوئیز (Quiz Responses)

### لیست پاسخ‌ها

**Endpoint:**
```
GET /api/quiz-responses/
```

---

### جزئیات پاسخ

**Endpoint:**
```
GET /api/quiz-responses/{id}/
```

**Response:**
```json
{
  "id": 1,
  "quiz": 1,
  "question": 1,
  "answer": 2,
  "score": 1.0,
  "done": "completed",
  "question_details": {
    "id": 1,
    "description": "سوال اول؟",
    ...
  }
}
```

---

## 6. مدیریت ارزیابی پاسخ‌های کوئیز (Quiz Response Evaluations)

این جدول کارنامه کلی آزمون را نگهداری می‌کند (نمره درصدی).

### لیست ارزیابی‌ها

**Endpoint:**
```
GET /api/quiz-response-evaluations/
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "quiz": 1,
    "score": 80.5,
    "quiz_details": {...},
    "user_name": "نام کاربر"
  }
]
```

**نکته:** فیلد `score` نمره به صورت درصد است (0-100).

---

## مثال استفاده

### شروع یک کوئیز

```javascript
// شروع کوئیز
const startResponse = await fetch('http://localhost:8000/api/quizzes/start/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    evaluation_id: 1
  })
});

const { quiz, questions } = await startResponse.json();
console.log('کوئیز شروع شد:', quiz);
console.log('سوالات:', questions);

// ذخیره quiz_id برای ارسال پاسخ‌ها
const quizId = quiz.id;
```

### ارسال پاسخ‌ها

```javascript
// آماده کردن پاسخ‌ها
const responses = questions.map(question => ({
  question_id: question.id,
  answer: selectedAnswers[question.id], // پاسخ انتخاب شده توسط کاربر
  done: 'completed'
}));

// ارسال پاسخ‌ها
const submitResponse = await fetch('http://localhost:8000/api/quizzes/submit/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    quiz_id: quizId,
    responses: responses
  })
});

const result = await submitResponse.json();
console.log('نتیجه:', result.result);
console.log('نمره:', result.result.percentage);
console.log('وضعیت قبولی:', result.result.is_accept);
```

### دریافت نتیجه کوئیز

```javascript
const resultResponse = await fetch(`http://localhost:8000/api/quizzes/${quizId}/result/`, {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const result = await resultResponse.json();
console.log('نتیجه نهایی:', result);
```

---

## فلوچارت فرآیند آزمون

```
1. دریافت لیست ارزیابی‌ها
   GET /api/evaluations/

2. شروع کوئیز
   POST /api/quizzes/start/
   Body: { "evaluation_id": 1 }

3. دریافت سوالات (اختیاری - اگر قبلاً دریافت نشده)
   GET /api/quizzes/{id}/questions/

4. ارسال پاسخ‌ها
   POST /api/quizzes/submit/
   Body: { "quiz_id": 1, "responses": [...] }

5. دریافت نتیجه
   GET /api/quizzes/{id}/result/
```

---

## کدهای خطا

- **200 OK**: درخواست موفق
- **201 Created**: ایجاد موفق
- **400 Bad Request**: 
  - کوئیز فعال دیگری وجود دارد
  - تعداد پاسخ‌ها با تعداد سوالات مطابقت ندارد
  - کوئیز قبلاً تمام شده است
- **401 Unauthorized**: عدم احراز هویت
- **403 Forbidden**: عدم دسترسی
- **404 Not Found**: ارزیابی یا کوئیز یافت نشد
- **429 Too Many Requests**: تعداد درخواست‌ها بیش از حد مجاز

---

## Rate Limiting

- **GET requests**: 100 درخواست در ساعت
- **POST/PUT/PATCH/DELETE**: 50 درخواست در ساعت
- **Start Quiz**: 20 درخواست در ساعت
- **Submit Quiz**: 20 درخواست در ساعت

---

## نکات مهم

1. **یک کوئیز فعال در هر زمان:** برای هر evaluation، فقط یک کوئیز فعال می‌تواند وجود داشته باشد.

2. **انتخاب تصادفی سوالات:** سوالات به صورت تصادفی از بانک سوالات انتخاب می‌شوند.

3. **محاسبه خودکار نمره:** پس از ارسال پاسخ‌ها، نمره به صورت خودکار محاسبه می‌شود.

4. **ثبت خودکار MissionResult:** اگر کاربر در آزمون قبول شود و ماموریت مرتبطی وجود داشته باشد، نتیجه ماموریت به صورت خودکار ثبت می‌شود.

5. **عدم نمایش پاسخ صحیح:** در سوالات کوئیز، پاسخ صحیح نمایش داده نمی‌شود (فقط برای مدرسان در endpoint سوالات ارزیابی).
