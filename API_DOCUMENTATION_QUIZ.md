# مستندات کامل سیستم آزمون و کوئیز

## فهرست مطالب
1. [معرفی سیستم](#معرفی-سیستم)
2. [فرآیند کلی سیستم](#فرآیند-کلی-سیستم)
3. [API Endpoints](#api-endpoints)
4. [سناریوهای استفاده](#سناریوهای-استفاده)
5. [نمونه درخواست‌ها و پاسخ‌ها](#نمونه-درخواست‌ها-و-پاسخ‌ها)

---

## معرفی سیستم

سیستم آزمون و کوئیز یک پلتفرم جامع برای مدیریت آزمون‌های آنلاین است که امکان ایجاد، مدیریت و شرکت در آزمون‌ها را برای مدرسان و دانشجویان فراهم می‌کند.

### قابلیت‌های اصلی سیستم:

1. **مدیریت Evaluation (ارزیابی)**: مدرسان می‌توانند آزمون‌های جدید ایجاد کنند و مشخصات آن‌ها را تعیین نمایند
2. **بانک سوالات**: هر Evaluation دارای یک بانک سوالات است که مدرس می‌تواند سوالات را به آن اضافه کند
3. **ایجاد کوئیز تصادفی**: هنگام شرکت دانشجو در آزمون، سیستم به صورت خودکار سوالات را به صورت تصادفی انتخاب می‌کند
4. **ارزیابی خودکار**: سیستم به صورت خودکار پاسخ‌های دانشجو را بررسی و نمره‌دهی می‌کند
5. **گزارش‌دهی**: کارنامه کامل دانشجو شامل درصد پاسخ صحیح و نمره نهایی محاسبه و ذخیره می‌شود

---

## فرآیند کلی سیستم

### مرحله 1: ایجاد Evaluation توسط مدرس
مدرس یک Evaluation جدید ایجاد می‌کند و مشخصات زیر را تعیین می‌کند:
- تعداد سوالات مورد نیاز (`number_of_question`)
- نمره قبولی (`accept_score`)
- مدت زمان آزمون (`duration`)
- و سایر مشخصات

### مرحله 2: ایجاد بانک سوالات
مدرس با استفاده از API مربوط به Question، سوالات را به Evaluation اضافه می‌کند. هر سوال شامل:
- متن سوال (`description`)
- گزینه‌های پاسخ (`c1`, `c2`, `c3`, `c4`)
- پاسخ صحیح (`correct`)
- وزن سوال (`weight`)

### مرحله 3: شرکت دانشجو در آزمون
دانشجو با استفاده از API `/api/quizzes/start/` در آزمون شرکت می‌کند. سیستم:
- یک Quiz جدید ایجاد می‌کند
- به تعداد `number_of_question` از سوالات Evaluation را به صورت تصادفی انتخاب می‌کند
- سوالات انتخاب شده را به دانشجو نمایش می‌دهد

### مرحله 4: پاسخ‌دهی به سوالات
دانشجو به سوالات پاسخ می‌دهد و می‌تواند پاسخ‌های خود را ذخیره کند.

### مرحله 5: اتمام آزمون و ارسال پاسخ‌ها
دانشجو با استفاده از API `/api/quizzes/submit/` تمام پاسخ‌های خود را ارسال می‌کند. سیستم:
- هر پاسخ را با پاسخ صحیح مقایسه می‌کند
- نمره هر سوال را محاسبه می‌کند (بر اساس `weight` یا 1 به صورت پیش‌فرض)
- نمره کل را محاسبه می‌کند
- درصد پاسخ صحیح را محاسبه می‌کند
- وضعیت قبولی/رد را تعیین می‌کند
- تمام اطلاعات را در جداول مربوطه ذخیره می‌کند

### مرحله 6: مشاهده کارنامه
دانشجو و مدرس می‌توانند با استفاده از API `/api/quizzes/{id}/result/` کارنامه کامل را مشاهده کنند.

---

## API Endpoints

### 1. مدیریت Evaluation

#### 1.1. لیست Evaluation ها
```
GET /api/evaluations/
```
**توضیحات**: دریافت لیست تمام Evaluation های موجود

**پارامترهای Query (اختیاری)**:
- `mission_id`: فیلتر بر اساس Mission
- `is_active`: فیلتر بر اساس وضعیت فعال/غیرفعال

**پاسخ موفق** (200):
```json
[
  {
    "id": 1,
    "type": true,
    "acceptscore": 70,
    "numberofquestion": 10,
    "missionid": 1,
    "userid": 5,
    "createat": "2024-01-15T10:00:00Z",
    "isactive": true,
    "canback": true,
    "duration": 60,
    "questions_count": 25
  }
]
```

#### 1.2. ایجاد Evaluation جدید
```
POST /api/evaluations/
```
**توضیحات**: ایجاد یک Evaluation جدید توسط مدرس

**Body**:
```json
{
  "type": true,
  "acceptscore": 70,
  "numberofquestion": 10,
  "missionid": 1,
  "userid": 5,
  "isactive": true,
  "canback": true,
  "duration": 60
}
```

**پاسخ موفق** (201):
```json
{
  "id": 1,
  "type": true,
  "acceptscore": 70,
  "numberofquestion": 10,
  "missionid": 1,
  "userid": 5,
  "createat": "2024-01-15T10:00:00Z",
  "isactive": true,
  "canback": true,
  "duration": 60,
  "questions_count": 0
}
```

#### 1.3. دریافت جزئیات یک Evaluation
```
GET /api/evaluations/{id}/
```

#### 1.4. به‌روزرسانی Evaluation
```
PUT /api/evaluations/{id}/
PATCH /api/evaluations/{id}/
```

#### 1.5. حذف Evaluation
```
DELETE /api/evaluations/{id}/
```

---

### 2. مدیریت سوالات (Question)

#### 2.1. لیست سوالات
```
GET /api/questions/
```
**توضیحات**: دریافت لیست تمام سوالات

**پارامترهای Query (اختیاری)**:
- `evaluation_id`: فیلتر بر اساس Evaluation

**پاسخ موفق** (200):
```json
[
  {
    "id": 1,
    "evaluationid": 1,
    "description": "پایتخت ایران کجاست؟",
    "img": null,
    "type": true,
    "c1": "تهران",
    "c2": "اصفهان",
    "c3": "شیراز",
    "c4": "مشهد",
    "correct": 1,
    "answer": null,
    "weight": 1.0,
    "canshuffle": false
  }
]
```

#### 2.2. ایجاد سوال جدید
```
POST /api/questions/
```
**توضیحات**: اضافه کردن سوال جدید به بانک سوالات یک Evaluation

**Body**:
```json
{
  "evaluationid": 1,
  "description": "پایتخت ایران کجاست؟",
  "img": null,
  "type": true,
  "c1": "تهران",
  "c2": "اصفهان",
  "c3": "شیراز",
  "c4": "مشهد",
  "correct": 1,
  "answer": null,
  "weight": 1.0,
  "canshuffle": false
}
```

**نکات مهم**:
- `evaluationid`: باید به یک Evaluation معتبر اشاره کند
- `correct`: شماره گزینه صحیح (1 تا 4)
- `weight`: وزن سوال در محاسبه نمره (پیش‌فرض: 1.0)
- `type`: نوع سوال (true برای چندگزینه‌ای)

**پاسخ موفق** (201):
```json
{
  "id": 1,
  "evaluationid": 1,
  "description": "پایتخت ایران کجاست؟",
  "img": null,
  "type": true,
  "c1": "تهران",
  "c2": "اصفهان",
  "c3": "شیراز",
  "c4": "مشهد",
  "correct": 1,
  "answer": null,
  "weight": 1.0,
  "canshuffle": false
}
```

#### 2.3. دریافت جزئیات یک سوال
```
GET /api/questions/{id}/
```

#### 2.4. به‌روزرسانی سوال
```
PUT /api/questions/{id}/
PATCH /api/questions/{id}/
```

#### 2.5. حذف سوال
```
DELETE /api/questions/{id}/
```

---

### 3. مدیریت کوئیز (Quiz)

#### 3.1. شروع کوئیز جدید ⭐
```
POST /api/quizzes/start/
```
**توضیحات**: این endpoint اصلی ترین بخش سیستم است. دانشجو با استفاده از این API در یک Evaluation شرکت می‌کند و سیستم به صورت خودکار:
- یک Quiz جدید ایجاد می‌کند
- به تعداد `number_of_question` از سوالات Evaluation را به صورت تصادفی انتخاب می‌کند
- سوالات را به دانشجو برمی‌گرداند (بدون نمایش پاسخ صحیح)

**Body**:
```json
{
  "evaluation_id": 1
}
```

**پاسخ موفق** (201):
```json
{
  "quiz": {
    "id": 1,
    "evaluationid": 1,
    "userid": 10,
    "startat": "2024-01-15T10:30:00Z",
    "endat": null,
    "score": null,
    "isaccept": null,
    "state": "started",
    "evaluation_details": {
      "id": 1,
      "type": true,
      "acceptscore": 70,
      "numberofquestion": 10,
      "duration": 60,
      "questions_count": 25
    },
    "responses_count": 10
  },
  "questions": [
    {
      "id": 5,
      "description": "پایتخت ایران کجاست؟",
      "img": null,
      "type": true,
      "c1": "تهران",
      "c2": "اصفهان",
      "c3": "شیراز",
      "c4": "مشهد",
      "weight": 1.0,
      "canshuffle": false
    },
    ...
  ],
  "message": "کوئیز با موفقیت ایجاد شد"
}
```

**خطاهای ممکن**:
- `400`: Evaluation یافت نشد یا غیرفعال است
- `400`: تعداد سوالات موجود کمتر از تعداد مورد نیاز است
- `400`: یک کوئیز فعال برای این evaluation دارید
- `403`: دسترسی به این evaluation ندارید

**نکات مهم**:
- اگر دانشجو قبلاً یک کوئیز فعال برای این Evaluation داشته باشد، خطا برمی‌گرداند
- سوالات به صورت تصادفی انتخاب می‌شوند
- پاسخ صحیح (`correct`) در سوالات نمایش داده نمی‌شود

#### 3.2. دریافت سوالات یک کوئیز
```
GET /api/quizzes/{id}/questions/
```
**توضیحات**: دریافت سوالات یک کوئیز فعال به همراه پاسخ‌های فعلی (در صورت وجود)

**پاسخ موفق** (200):
```json
{
  "quiz_id": 1,
  "evaluation_id": 1,
  "start_at": "2024-01-15T10:30:00Z",
  "end_at": null,
  "state": "started",
  "questions": [
    {
      "id": 5,
      "description": "پایتخت ایران کجاست؟",
      "img": null,
      "type": true,
      "c1": "تهران",
      "c2": "اصفهان",
      "c3": "شیراز",
      "c4": "مشهد",
      "weight": 1.0,
      "canshuffle": false,
      "current_answer": 1,
      "done": "completed"
    },
    ...
  ]
}
```

#### 3.3. ارسال پاسخ‌های کوئیز ⭐
```
POST /api/quizzes/submit/
```
**توضیحات**: این endpoint پاسخ‌های دانشجو را دریافت می‌کند و:
- هر پاسخ را با پاسخ صحیح مقایسه می‌کند
- نمره هر سوال را محاسبه می‌کند
- نمره کل و درصد پاسخ صحیح را محاسبه می‌کند
- وضعیت قبولی/رد را تعیین می‌کند
- تمام اطلاعات را ذخیره می‌کند

**Body**:
```json
{
  "quiz_id": 1,
  "responses": [
    {
      "question_id": 5,
      "answer": 1,
      "done": "completed"
    },
    {
      "question_id": 7,
      "answer": 3,
      "done": "completed"
    },
    ...
  ]
}
```

**پارامترها**:
- `quiz_id`: شناسه کوئیز
- `responses`: آرایه‌ای از پاسخ‌ها
  - `question_id`: شناسه سوال
  - `answer`: شماره گزینه انتخاب شده (1 تا 4) یا null
  - `done`: وضعیت انجام (اختیاری)

**پاسخ موفق** (200):
```json
{
  "message": "پاسخ‌های کوئیز با موفقیت ثبت شد",
  "result": {
    "quiz_id": 1,
    "total_questions": 10,
    "correct_answers": 7,
    "wrong_answers": 3,
    "percentage": 70.0,
    "total_score": 7.0,
    "is_accept": true,
    "accept_score": 70,
    "responses": [
      {
        "id": 1,
        "quizid": 1,
        "questionid": 5,
        "answer": 1,
        "score": 1.0,
        "done": "completed",
        "question_details": {
          "id": 5,
          "description": "پایتخت ایران کجاست؟",
          "correct": 1,
          ...
        }
      },
      ...
    ]
  }
}
```

**خطاهای ممکن**:
- `400`: تعداد پاسخ‌های ارسالی با تعداد سوالات مطابقت ندارد
- `400`: این کوئیز قبلاً تمام شده است
- `403`: شما دسترسی به این کوئیز ندارید
- `404`: کوئیز یافت نشد

**نکات مهم**:
- تمام سوالات باید پاسخ داده شوند (حتی اگر null باشد)
- نمره هر سوال بر اساس `weight` محاسبه می‌شود (پیش‌فرض: 1.0)
- اگر `total_score >= accept_score` باشد، `is_accept = true`

#### 3.4. دریافت نتیجه کوئیز ⭐
```
GET /api/quizzes/{id}/result/
```
**توضیحات**: دریافت کارنامه کامل کوئیز شامل:
- تعداد سوالات کل
- تعداد پاسخ‌های صحیح و غلط
- درصد پاسخ صحیح
- نمره کل
- وضعیت قبولی/رد
- جزئیات تمام پاسخ‌ها

**پاسخ موفق** (200):
```json
{
  "quiz_id": 1,
  "total_questions": 10,
  "correct_answers": 7,
  "wrong_answers": 3,
  "percentage": 70.0,
  "total_score": 7.0,
  "is_accept": true,
  "accept_score": 70,
  "start_at": "2024-01-15T10:30:00Z",
  "end_at": "2024-01-15T11:00:00Z",
  "responses": [
    {
      "id": 1,
      "quizid": 1,
      "questionid": 5,
      "answer": 1,
      "score": 1.0,
      "done": "completed",
      "question_details": {
        "id": 5,
        "description": "پایتخت ایران کجاست؟",
        "correct": 1,
        "c1": "تهران",
        "c2": "اصفهان",
        "c3": "شیراز",
        "c4": "مشهد",
        "weight": 1.0
      }
    },
    ...
  ]
}
```

**خطاهای ممکن**:
- `400`: این کوئیز هنوز تمام نشده است
- `403`: دسترسی به این کوئیز ندارید
- `404`: کوئیز یافت نشد

#### 3.5. لیست کوئیزها
```
GET /api/quizzes/
```
**توضیحات**: دریافت لیست تمام کوئیزهای کاربر

**پارامترهای Query (اختیاری)**:
- `evaluation_id`: فیلتر بر اساس Evaluation
- `user_id`: فیلتر بر اساس کاربر
- `state`: فیلتر بر اساس وضعیت (started, completed, ...)

#### 3.6. دریافت جزئیات یک کوئیز
```
GET /api/quizzes/{id}/
```

#### 3.7. به‌روزرسانی کوئیز
```
PUT /api/quizzes/{id}/
PATCH /api/quizzes/{id}/
```

#### 3.8. حذف کوئیز
```
DELETE /api/quizzes/{id}/
```

---

### 4. مدیریت پاسخ‌های کوئیز (QuizResponse)

#### 4.1. لیست پاسخ‌ها
```
GET /api/quiz-responses/
```
**توضیحات**: دریافت لیست تمام پاسخ‌های کوئیز

**پارامترهای Query (اختیاری)**:
- `quiz_id`: فیلتر بر اساس Quiz

#### 4.2. دریافت جزئیات یک پاسخ
```
GET /api/quiz-responses/{id}/
```

#### 4.3. به‌روزرسانی پاسخ
```
PUT /api/quiz-responses/{id}/
PATCH /api/quiz-responses/{id}/
```

**نکته**: معمولاً نیازی به استفاده مستقیم از این endpoint نیست، زیرا پاسخ‌ها از طریق `/api/quizzes/submit/` ثبت می‌شوند.

---

### 5. مدیریت ارزیابی پاسخ‌ها (QuizResponseEvaluation)

#### 5.1. لیست ارزیابی‌ها
```
GET /api/quiz-response-evaluations/
```

#### 5.2. دریافت جزئیات یک ارزیابی
```
GET /api/quiz-response-evaluations/{id}/
```

**نکته**: این رکوردها به صورت خودکار هنگام ارسال پاسخ‌ها ایجاد می‌شوند.

---

## سناریوهای استفاده

### سناریو 1: مدرس یک آزمون جدید ایجاد می‌کند

1. **ایجاد Evaluation**:
   ```
   POST /api/evaluations/
   {
     "type": true,
     "acceptscore": 70,
     "numberofquestion": 10,
     "missionid": 1,
     "userid": 5,
     "isactive": true,
     "canback": true,
     "duration": 60
   }
   ```
   پاسخ: `evaluation_id = 1`

2. **اضافه کردن سوالات**:
   ```
   POST /api/questions/
   {
     "evaluationid": 1,
     "description": "پایتخت ایران کجاست؟",
     "type": true,
     "c1": "تهران",
     "c2": "اصفهان",
     "c3": "شیراز",
     "c4": "مشهد",
     "correct": 1,
     "weight": 1.0
   }
   ```
   (این کار را برای 25 سوال تکرار می‌کند)

### سناریو 2: دانشجو در آزمون شرکت می‌کند

1. **شروع کوئیز**:
   ```
   POST /api/quizzes/start/
   {
     "evaluation_id": 1
   }
   ```
   پاسخ: کوئیز ایجاد شد و 10 سوال تصادفی برگردانده شد

2. **دریافت سوالات** (در صورت نیاز):
   ```
   GET /api/quizzes/1/questions/
   ```

3. **ارسال پاسخ‌ها**:
   ```
   POST /api/quizzes/submit/
   {
     "quiz_id": 1,
     "responses": [
       {"question_id": 5, "answer": 1},
       {"question_id": 7, "answer": 3},
       ...
     ]
   }
   ```
   پاسخ: نمره و کارنامه محاسبه شد

4. **مشاهده کارنامه**:
   ```
   GET /api/quizzes/1/result/
   ```

### سناریو 3: مدرس نتایج دانشجویان را بررسی می‌کند

1. **لیست کوئیزهای یک Evaluation**:
   ```
   GET /api/quizzes/?evaluation_id=1
   ```

2. **مشاهده کارنامه هر دانشجو**:
   ```
   GET /api/quizzes/{quiz_id}/result/
   ```

---

## نمونه درخواست‌ها و پاسخ‌ها

### مثال کامل: از شروع تا پایان

#### مرحله 1: ایجاد Evaluation
```bash
curl -X POST http://localhost:8000/api/evaluations/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": true,
    "acceptscore": 70,
    "numberofquestion": 5,
    "missionid": 1,
    "userid": 5,
    "isactive": true,
    "canback": true,
    "duration": 30
  }'
```

#### مرحله 2: اضافه کردن سوالات
```bash
curl -X POST http://localhost:8000/api/questions/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluationid": 1,
    "description": "2 + 2 برابر است با؟",
    "type": true,
    "c1": "3",
    "c2": "4",
    "c3": "5",
    "c4": "6",
    "correct": 2,
    "weight": 1.0
  }'
```

#### مرحله 3: شروع کوئیز
```bash
curl -X POST http://localhost:8000/api/quizzes/start/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_id": 1
  }'
```

#### مرحله 4: ارسال پاسخ‌ها
```bash
curl -X POST http://localhost:8000/api/quizzes/submit/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_id": 1,
    "responses": [
      {"question_id": 1, "answer": 2, "done": "completed"},
      {"question_id": 2, "answer": 1, "done": "completed"},
      {"question_id": 3, "answer": 3, "done": "completed"},
      {"question_id": 4, "answer": 2, "done": "completed"},
      {"question_id": 5, "answer": 4, "done": "completed"}
    ]
  }'
```

#### مرحله 5: مشاهده نتیجه
```bash
curl -X GET http://localhost:8000/api/quizzes/1/result/ \
  -H "Authorization: Bearer {token}"
```

---

## نکات مهم و بهترین روش‌ها

### امنیت
- تمام endpoint ها نیاز به احراز هویت دارند (JWT Token)
- کاربران فقط به داده‌های شرکت خود دسترسی دارند (مگر Admin)
- Rate limiting برای جلوگیری از سوء استفاده اعمال شده است

### عملکرد
- استفاده از `select_related` و `prefetch_related` برای بهینه‌سازی query ها
- استفاده از transaction برای اطمینان از یکپارچگی داده‌ها

### اعتبارسنجی
- بررسی تعداد سوالات قبل از ایجاد کوئیز
- بررسی تکمیل بودن پاسخ‌ها قبل از ارسال
- بررسی دسترسی کاربر به Evaluation و Quiz

### خطاها
- تمام خطاها با پیام‌های واضح فارسی برگردانده می‌شوند
- کدهای وضعیت HTTP مناسب استفاده شده است

---

## خلاصه قابلیت‌های سیستم

✅ **ایجاد و مدیریت Evaluation**: مدرسان می‌توانند آزمون‌های جدید ایجاد کنند

✅ **بانک سوالات**: امکان اضافه کردن سوالات نامحدود به هر Evaluation

✅ **انتخاب تصادفی سوالات**: سیستم به صورت خودکار سوالات را انتخاب می‌کند

✅ **ارزیابی خودکار**: محاسبه نمره و درصد پاسخ صحیح به صورت خودکار

✅ **کارنامه کامل**: نمایش جزئیات کامل نتایج آزمون

✅ **مدیریت دسترسی**: کنترل دسترسی بر اساس شرکت و نقش کاربر

✅ **Rate Limiting**: جلوگیری از سوء استفاده از API

✅ **Transaction Safety**: اطمینان از یکپارچگی داده‌ها در عملیات‌های پیچیده

---

## پشتیبانی

برای سوالات و مشکلات، لطفاً با تیم توسعه تماس بگیرید.

---

**نسخه مستندات**: 1.0  
**تاریخ به‌روزرسانی**: 2024-01-15

