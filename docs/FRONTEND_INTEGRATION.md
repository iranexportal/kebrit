# راهنمای یکپارچه‌سازی Frontend با API Kebrit

این مستندات برای تیم Frontend نوشته شده است تا بتوانند صفحه آزمون را پیاده‌سازی کنند.

## جریان کلی (Flow)

1. کاربر از سایت مشتری روی "شروع آزمون" کلیک می‌کند
2. سرور مشتری درخواست `POST /api/integration/exams/launch/` را ارسال می‌کند
3. API یک `quiz_id` و `redirect_url` برمی‌گرداند
4. کاربر به `redirect_url` منتقل می‌شود (که شامل `token` در query parameter است)
5. Frontend صفحه آزمون را نمایش می‌دهد و سوالات را با `quiz_id` دریافت می‌کند
6. کاربر پاسخ‌ها را می‌دهد و submit می‌کند
7. Frontend به `callback_url` مشتری redirect می‌کند

---

## مراحل پیاده‌سازی

### مرحله 1: دریافت quiz_id و token

وقتی کاربر از سایت مشتری به صفحه آزمون منتقل می‌شود، URL به این شکل است:

```
http://localhost:3000/quiz/{quiz_id}?token={access_token}
```

در response از `/api/integration/exams/launch/` یک `quiz_id` برگردانده می‌شود:

```javascript
// Response از /api/integration/exams/launch/
{
  "launch_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // برای رجوع داخلی
  "quiz_id": 66,
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "redirect_url": "http://localhost:3000/quiz/66?token=eyJhbGciOiJIUzI1NiIs..."
}
```

**نکته مهم:** 
- از `quiz_id` برای تمام درخواست‌ها استفاده کنید
- اگر `token` در URL وجود دارد، آن را استخراج کنید و در header قرار دهید: `Authorization: Bearer {token}` (اختیاری)

---

### مرحله 2: دریافت سوالات آزمون

از `quiz_id` برای دریافت سوالات استفاده کنید:

```javascript
// GET /api/quiz/{quiz_id}/
const quizId = 66; // از URL یا response قبلی

fetch(`http://localhost:8000/api/quiz/${quizId}/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // data.questions شامل سوالات است
  // data.evaluation شامل اطلاعات آزمون است
  console.log('Questions:', data.questions);
  console.log('Evaluation:', data.evaluation);
});
```

**نکته:** این endpoint نیاز به JWT token ندارد. فقط `quiz_id` کافی است.

---

### مرحله 3: ذخیره پاسخ‌ها (اختیاری - برای ذخیره تدریجی)

می‌توانید پاسخ‌ها را به صورت تدریجی ذخیره کنید:

```javascript
// POST /api/quiz/{quiz_id}/answer/
const quizId = 66;

fetch(`http://localhost:8000/api/quiz/${quizId}/answer/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question_id: 1,
    answer: "2", // برای چندگزینه‌ای: عدد به صورت string
    done: "in_progress" // یا "completed"
  })
})
.then(response => response.json())
.then(data => {
  console.log('Answer saved:', data.message);
});
```

---

### مرحله 4: ارسال نهایی آزمون (Submit)

**⚠️ مهم:** از endpoint `/api/quiz/{quiz_id}/submit/` استفاده کنید، نه `/api/quizzes/submit/`

```javascript
// POST /api/quiz/{quiz_id}/submit/
const quizId = 66;

// آماده‌سازی پاسخ‌ها
const responses = [
  { question_id: 1, answer: "2", done: "completed" }, // چندگزینه‌ای: عدد به صورت string
  { question_id: 2, answer: "4", done: "completed" },
  { question_id: 3, answer: "پاسخ تشریحی...", done: "completed" } // تشریحی: متن
];

fetch(`http://localhost:8000/api/quiz/${quizId}/submit/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    responses: responses
  })
})
.then(response => response.json())
.then(data => {
  if (data.redirect_url) {
    // نمایش نتیجه به کاربر
    console.log('Result:', data.result);
    console.log('Percentage:', data.result.percentage);
    console.log('Is Accept:', data.result.is_accept);
    
    // Redirect به callback_url مشتری
    window.location.href = data.redirect_url;
    
    // یا می‌توانید از endpoint redirect استفاده کنید:
    // window.location.href = `http://localhost:8000/api/quiz/${quizId}/redirect/`;
  }
})
.catch(error => {
  console.error('Error:', error);
});
```

**Response از submit:**
```json
{
  "message": "پاسخ‌ها ثبت و آزمون پایان یافت",
  "result": {
    "quiz_id": 66,
    "total_questions": 20,
    "correct_answers": 14,
    "wrong_answers": 6,
    "percentage": 70.0,
    "total_score": 14.0,
    "is_accept": true,
    "state": "completed",
    "responses": [...]
  },
  "redirect_url": "https://client.example.com/exam/callback?student_uuid=...&mobile=...&eurl=12&quiz_id=66&percentage=70&total_score=14&is_accept=True&state=completed&launch_id=..."
}
```

---

### مرحله 5: Redirect به callback_url

بعد از submit، دو روش برای redirect وجود دارد:

#### روش 1: استفاده از redirect_url از response (پیشنهادی)

```javascript
// بعد از submit موفق
if (data.redirect_url) {
  window.location.href = data.redirect_url;
}
```

#### روش 2: استفاده از endpoint redirect

```javascript
// GET /api/quiz/{quiz_id}/redirect/
window.location.href = `http://localhost:8000/api/quiz/${quizId}/redirect/`;
```

این endpoint یک HTTP 302 redirect انجام می‌دهد و کاربر را به `callback_url` مشتری منتقل می‌کند.

---

## ساختار داده‌ها

### سوال (Question)

```typescript
interface Question {
  id: number;
  text: string;
  type: boolean; // true = چندگزینه‌ای, false = تشریحی
  c1?: string; // گزینه 1 (فقط برای چندگزینه‌ای)
  c2?: string; // گزینه 2
  c3?: string; // گزینه 3
  c4?: string; // گزینه 4
  weight?: number; // وزن سوال
  can_shuffle?: boolean;
  current_answer?: string | null; // پاسخ فعلی کاربر
  done?: string | null; // وضعیت: "in_progress" | "completed" | null
}
```

### پاسخ (Response)

```typescript
interface Response {
  question_id: number;
  answer: string | null; // برای چندگزینه‌ای: عدد به صورت string ("1", "2", ...), برای تشریحی: متن
  done: "in_progress" | "completed";
}
```

### نتیجه آزمون (Result)

```typescript
interface QuizResult {
  quiz_id: number;
  total_questions: number;
  correct_answers: number;
  wrong_answers: number;
  percentage: number;
  total_score: number;
  is_accept: boolean;
  state: "completed" | "pending";
  responses: Array<{
    id: number;
    quiz: number;
    question: number;
    answer: string | null;
    score: number;
    done: string;
  }>;
}
```

---

## Callback URL Parameters

وقتی کاربر به `callback_url` مشتری redirect می‌شود، این پارامترها در query string اضافه می‌شوند:

- `student_uuid`: شناسه یکتا دانشجو
- `mobile`: شماره موبایل دانشجو
- `eurl`: شناسه آزمون (evaluation id)
- `quiz_id`: شناسه کوئیز
- `percentage`: درصد نمره
- `total_score`: نمره کل
- `is_accept`: آیا قبول شده است (true/false)
- `state`: وضعیت آزمون ("completed" یا "pending")
- `launch_id`: شناسه launch

مثال:
```
https://client.example.com/exam/callback?student_uuid=73979&mobile=09123456789&eurl=12&quiz_id=66&percentage=70&total_score=14&is_accept=True&state=completed&launch_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## مدیریت خطاها

### خطای 404 - Launch یافت نشد

```javascript
if (response.status === 404) {
  // نمایش پیام خطا به کاربر
  alert('آزمون یافت نشد. لطفاً دوباره تلاش کنید.');
}
```

### خطای 400 - آزمون قبلاً تمام شده

```javascript
if (response.status === 400) {
  const error = await response.json();
  if (error.error === 'این آزمون قبلاً تمام شده است') {
    // نمایش نتیجه قبلی یا redirect به callback
  }
}
```

### خطای 400 - تعداد پاسخ‌ها مطابقت ندارد

```javascript
if (response.status === 400) {
  const error = await response.json();
  if (error.error.includes('تعداد پاسخ‌های ارسالی')) {
    // بررسی کنید که تمام سوالات پاسخ داده شده باشند
  }
}
```

---

## مثال کامل (Complete Example)

```javascript
// 1. دریافت quiz_id از URL یا response قبلی
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
// quiz_id از URL path استخراج می‌شود: /quiz/{quiz_id}
const pathParts = window.location.pathname.split('/');
const quizId = parseInt(pathParts[pathParts.length - 1]); // یا از response قبلی

// 2. دریافت سوالات
async function loadQuestions() {
  const response = await fetch(`http://localhost:8000/api/quiz/${quizId}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to load questions');
  }
  
  const data = await response.json();
  return data;
}

// 3. ذخیره پاسخ یک سوال (اختیاری)
async function saveAnswer(questionId, answer, done = 'in_progress') {
  const response = await fetch(`http://localhost:8000/api/quiz/${quizId}/answer/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      question_id: questionId,
      answer: answer,
      done: done
    })
  });
  
  return response.json();
}

// 4. ارسال نهایی
async function submitQuiz(responses) {
  const response = await fetch(`http://localhost:8000/api/quiz/${quizId}/submit/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      responses: responses
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to submit quiz');
  }
  
  const data = await response.json();
  
  // نمایش نتیجه
  console.log('Quiz completed!');
  console.log('Percentage:', data.result.percentage);
  console.log('Is Accept:', data.result.is_accept);
  
  // Redirect به callback_url
  if (data.redirect_url) {
    window.location.href = data.redirect_url;
  }
  
  return data;
}

// استفاده
(async () => {
  try {
    // بارگذاری سوالات
    const quizData = await loadQuestions();
    console.log('Questions loaded:', quizData.questions);
    
    // آماده‌سازی پاسخ‌ها (مثال)
    const responses = quizData.questions.map(q => ({
      question_id: q.id,
      answer: q.current_answer || null,
      done: q.done || 'completed'
    }));
    
    // ارسال نهایی
    await submitQuiz(responses);
  } catch (error) {
    console.error('Error:', error);
    alert('خطا در ارسال آزمون: ' + error.message);
  }
})();
```

---

## نکات مهم

1. **همیشه از `/api/quiz/{quiz_id}/` endpoints استفاده کنید** - این endpoints نیاز به JWT ندارند
2. **از `/api/quizzes/submit/` استفاده نکنید** - این endpoint نیاز به JWT دارد و برای quiz-based flow مناسب نیست
3. **quiz_id را در تمام درخواست‌ها نگه دارید** - این شناسه برای دسترسی به آزمون لازم است
4. **بعد از submit، حتماً به redirect_url redirect کنید** - این URL شامل callback_url مشتری با تمام پارامترهای لازم است
5. **برای سوالات چندگزینه‌ای، answer را به صورت string ارسال کنید** (مثلاً "1", "2", "3", "4")
6. **برای سوالات تشریحی، answer را به صورت متن ارسال کنید**

---

## سوالات متداول (FAQ)

### Q: آیا نیاز به JWT token دارم؟

A: خیر! اگر از `/api/quiz/{quiz_id}/` endpoints استفاده کنید، نیازی به JWT ندارید. فقط `quiz_id` کافی است.

### Q: چگونه quiz_id را دریافت کنم؟

A: `quiz_id` در response از `/api/integration/exams/launch/` برگردانده می‌شود. این endpoint توسط سرور مشتری فراخوانی می‌شود. همچنین `quiz_id` در URL redirect نیز وجود دارد.

### Q: اگر token در URL باشد، باید از آن استفاده کنم؟

A: اختیاری است. اگر `quiz_id` دارید، نیازی به token نیست. اما می‌توانید token را در header قرار دهید: `Authorization: Bearer {token}`

### Q: چگونه می‌توانم پاسخ‌ها را به صورت تدریجی ذخیره کنم؟

A: از endpoint `/api/quiz/{quiz_id}/answer/` استفاده کنید. این endpoint برای ذخیره پاسخ یک سوال استفاده می‌شود.

### Q: بعد از submit چه اتفاقی می‌افتد؟

A: بعد از submit موفق، یک `redirect_url` در response برگردانده می‌شود که باید کاربر را به آن URL redirect کنید. این URL شامل callback_url مشتری با تمام پارامترهای نتیجه است.
