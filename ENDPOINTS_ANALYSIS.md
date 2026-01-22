# تحلیل کامل Endpoint های API

این سند شامل لیست کامل endpoint های API و تحلیل endpoint های مشابه است.

## آمار کلی

- **تعداد کل ViewSet ها**: 23
- **تعداد endpoint های استاندارد CRUD**: 138 (23 × 6)
- **تعداد endpoint های سفارشی**: 12
- **تعداد endpoint های یکتای غیر-CRUD**: 9
- **جمع کل endpoint ها**: 159

---

## 1. Endpoint های احراز هویت (Authentication)

### 1.1 JWT Token Endpoints
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| POST | `/api/token/` | دریافت JWT token (با mobile و token UUID) |
| POST | `/api/token/refresh/` | تازه‌سازی access token |
| POST | `/api/token/verify/` | بررسی اعتبار token |
| POST | `/api/token/logout/` | خروج از سیستم و blacklist کردن token |

### 1.2 Login Endpoint
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| POST | `/api/login/` | لاگین با mobile و token (بدون رمز عبور) |

**تحلیل**: 5 endpoint برای احراز هویت که همگی کار مشابه انجام می‌دهند (مدیریت session و token)

---

## 2. Users App Endpoints

### 2.1 Company ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/companies/` | لیست شرکت‌ها |
| POST | `/api/companies/` | ایجاد شرکت جدید |
| GET | `/api/companies/{id}/` | جزئیات یک شرکت |
| PUT | `/api/companies/{id}/` | به‌روزرسانی کامل شرکت |
| PATCH | `/api/companies/{id}/` | به‌روزرسانی جزئی شرکت |
| DELETE | `/api/companies/{id}/` | حذف شرکت |

### 2.2 User ViewSet (8 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/users/` | لیست کاربران |
| POST | `/api/users/` | ایجاد کاربر جدید |
| GET | `/api/users/{id}/` | جزئیات یک کاربر |
| PUT | `/api/users/{id}/` | به‌روزرسانی کامل کاربر |
| PATCH | `/api/users/{id}/` | به‌روزرسانی جزئی کاربر |
| DELETE | `/api/users/{id}/` | حذف کاربر |
| POST | `/api/users/create/` | ایجاد کاربر جدید با صدور token (سفارشی) |
| GET | `/api/users/company/{company_id}/` | لیست کاربران یک شرکت (سفارشی) |

### 2.3 Session ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/sessions/` | لیست session ها |
| POST | `/api/sessions/` | ایجاد session جدید |
| GET | `/api/sessions/{id}/` | جزئیات یک session |
| PUT | `/api/sessions/{id}/` | به‌روزرسانی کامل session |
| PATCH | `/api/sessions/{id}/` | به‌روزرسانی جزئی session |
| DELETE | `/api/sessions/{id}/` | حذف session |

### 2.4 Token ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/tokens/` | لیست token ها |
| POST | `/api/tokens/` | ایجاد token جدید |
| GET | `/api/tokens/{id}/` | جزئیات یک token |
| PUT | `/api/tokens/{id}/` | به‌روزرسانی کامل token |
| PATCH | `/api/tokens/{id}/` | به‌روزرسانی جزئی token |
| DELETE | `/api/tokens/{id}/` | حذف token |

### 2.5 Role ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/roles/` | لیست نقش‌ها |
| POST | `/api/roles/` | ایجاد نقش جدید |
| GET | `/api/roles/{id}/` | جزئیات یک نقش |
| PUT | `/api/roles/{id}/` | به‌روزرسانی کامل نقش |
| PATCH | `/api/roles/{id}/` | به‌روزرسانی جزئی نقش |
| DELETE | `/api/roles/{id}/` | حذف نقش |

### 2.6 UserRole ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/user-roles/` | لیست نقش‌های کاربران |
| POST | `/api/user-roles/` | اختصاص نقش به کاربر |
| GET | `/api/user-roles/{id}/` | جزئیات یک نقش کاربر |
| PUT | `/api/user-roles/{id}/` | به‌روزرسانی کامل نقش کاربر |
| PATCH | `/api/user-roles/{id}/` | به‌روزرسانی جزئی نقش کاربر |
| DELETE | `/api/user-roles/{id}/` | حذف نقش از کاربر |

**تحلیل Users App**: 38 endpoint که همگی عملیات CRUD استاندارد انجام می‌دهند (به جز 2 endpoint سفارشی)

---

## 3. Roadmap App Endpoints

### 3.1 Mission ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/missions/` | لیست ماموریت‌ها |
| POST | `/api/missions/` | ایجاد ماموریت جدید |
| GET | `/api/missions/{id}/` | جزئیات یک ماموریت |
| PUT | `/api/missions/{id}/` | به‌روزرسانی کامل ماموریت |
| PATCH | `/api/missions/{id}/` | به‌روزرسانی جزئی ماموریت |
| DELETE | `/api/missions/{id}/` | حذف ماموریت |

### 3.2 MissionRelation ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/mission-relations/` | لیست روابط ماموریت‌ها |
| POST | `/api/mission-relations/` | ایجاد رابطه جدید |
| GET | `/api/mission-relations/{id}/` | جزئیات یک رابطه |
| PUT | `/api/mission-relations/{id}/` | به‌روزرسانی کامل رابطه |
| PATCH | `/api/mission-relations/{id}/` | به‌روزرسانی جزئی رابطه |
| DELETE | `/api/mission-relations/{id}/` | حذف رابطه |

### 3.3 MissionResult ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/mission-results/` | لیست نتایج ماموریت‌ها |
| POST | `/api/mission-results/` | ایجاد نتیجه جدید |
| GET | `/api/mission-results/{id}/` | جزئیات یک نتیجه |
| PUT | `/api/mission-results/{id}/` | به‌روزرسانی کامل نتیجه |
| PATCH | `/api/mission-results/{id}/` | به‌روزرسانی جزئی نتیجه |
| DELETE | `/api/mission-results/{id}/` | حذف نتیجه |

### 3.4 Ability ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/abilities/` | لیست توانایی‌ها |
| POST | `/api/abilities/` | ایجاد توانایی جدید |
| GET | `/api/abilities/{id}/` | جزئیات یک توانایی |
| PUT | `/api/abilities/{id}/` | به‌روزرسانی کامل توانایی |
| PATCH | `/api/abilities/{id}/` | به‌روزرسانی جزئی توانایی |
| DELETE | `/api/abilities/{id}/` | حذف توانایی |

### 3.5 Custom Endpoint
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| POST | `/api/user-missions/` | دریافت ماموریت‌های انجام شده و در دسترس کاربر |

**تحلیل Roadmap App**: 25 endpoint که 24 تای آن CRUD استاندارد است

---

## 4. Exam App Endpoints

### 4.1 EvaluationType ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/evaluation-types/` | لیست انواع ارزیابی |
| POST | `/api/evaluation-types/` | ایجاد نوع ارزیابی جدید |
| GET | `/api/evaluation-types/{id}/` | جزئیات یک نوع ارزیابی |
| PUT | `/api/evaluation-types/{id}/` | به‌روزرسانی کامل نوع ارزیابی |
| PATCH | `/api/evaluation-types/{id}/` | به‌روزرسانی جزئی نوع ارزیابی |
| DELETE | `/api/evaluation-types/{id}/` | حذف نوع ارزیابی |

### 4.2 Evaluation ViewSet (7 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/evaluations/` | لیست ارزیابی‌ها |
| POST | `/api/evaluations/` | ایجاد ارزیابی جدید |
| GET | `/api/evaluations/{id}/` | جزئیات یک ارزیابی |
| PUT | `/api/evaluations/{id}/` | به‌روزرسانی کامل ارزیابی |
| PATCH | `/api/evaluations/{id}/` | به‌روزرسانی جزئی ارزیابی |
| DELETE | `/api/evaluations/{id}/` | حذف ارزیابی |
| GET | `/api/evaluations/{id}/questions/` | دریافت سوالات یک ارزیابی (سفارشی) |

### 4.3 Question ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/questions/` | لیست سوالات |
| POST | `/api/questions/` | ایجاد سوال جدید |
| GET | `/api/questions/{id}/` | جزئیات یک سوال |
| PUT | `/api/questions/{id}/` | به‌روزرسانی کامل سوال |
| PATCH | `/api/questions/{id}/` | به‌روزرسانی جزئی سوال |
| DELETE | `/api/questions/{id}/` | حذف سوال |

### 4.4 Quiz ViewSet (10 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/quizzes/` | لیست کوئیزها |
| POST | `/api/quizzes/` | ایجاد کوئیز جدید |
| GET | `/api/quizzes/{id}/` | جزئیات یک کوئیز |
| PUT | `/api/quizzes/{id}/` | به‌روزرسانی کامل کوئیز |
| PATCH | `/api/quizzes/{id}/` | به‌روزرسانی جزئی کوئیز |
| DELETE | `/api/quizzes/{id}/` | حذف کوئیز |
| POST | `/api/quizzes/start/` | شروع کوئیز جدید یا بازگردانی کوئیز فعال (سفارشی) |
| POST | `/api/quizzes/submit/` | ارسال پاسخ‌های کوئیز و محاسبه نمره (سفارشی) |
| GET | `/api/quizzes/{id}/questions/` | دریافت سوالات یک کوئیز فعال (سفارشی) |
| GET | `/api/quizzes/{id}/result/` | دریافت نتیجه نهایی کوئیز (سفارشی) |

### 4.5 QuizResponse ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/quiz-responses/` | لیست پاسخ‌های کوئیز |
| POST | `/api/quiz-responses/` | ایجاد پاسخ جدید |
| GET | `/api/quiz-responses/{id}/` | جزئیات یک پاسخ |
| PUT | `/api/quiz-responses/{id}/` | به‌روزرسانی کامل پاسخ |
| PATCH | `/api/quiz-responses/{id}/` | به‌روزرسانی جزئی پاسخ |
| DELETE | `/api/quiz-responses/{id}/` | حذف پاسخ |

### 4.6 QuizResponseEvaluation ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/quiz-response-evaluations/` | لیست ارزیابی‌های پاسخ کوئیز |
| POST | `/api/quiz-response-evaluations/` | ایجاد ارزیابی جدید |
| GET | `/api/quiz-response-evaluations/{id}/` | جزئیات یک ارزیابی |
| PUT | `/api/quiz-response-evaluations/{id}/` | به‌روزرسانی کامل ارزیابی |
| PATCH | `/api/quiz-response-evaluations/{id}/` | به‌روزرسانی جزئی ارزیابی |
| DELETE | `/api/quiz-response-evaluations/{id}/` | حذف ارزیابی |

### 4.7 Integration Endpoints (5 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/integration/exams/{eurl}/` | دریافت اطلاعات آزمون برای مشتری (با client token) |
| POST | `/api/integration/exams/launch/` | راه‌اندازی آزمون برای دانشجو (با client token) |
| GET | `/api/launch/{launch_id}/` | دریافت جزئیات و سوالات آزمون (برای دانشجو) |
| POST | `/api/launch/{launch_id}/answer/` | ذخیره یک پاسخ (برای دانشجو) |
| POST | `/api/launch/{launch_id}/submit/` | ارسال تمام پاسخ‌ها و نهایی‌سازی آزمون (برای دانشجو) |
| GET | `/api/launch/{launch_id}/redirect/` | ریدایرکت به callback URL مشتری |

**تحلیل Exam App**: 46 endpoint که شامل CRUD استاندارد و endpoint های سفارشی برای مدیریت کوئیز و integration است

---

## 5. Media App Endpoints

### 5.1 File ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/files/` | لیست فایل‌ها |
| POST | `/api/files/` | آپلود فایل جدید |
| GET | `/api/files/{id}/` | جزئیات یک فایل |
| PUT | `/api/files/{id}/` | به‌روزرسانی کامل فایل |
| PATCH | `/api/files/{id}/` | به‌روزرسانی جزئی فایل |
| DELETE | `/api/files/{id}/` | حذف فایل |

### 5.2 Tag ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/tags/` | لیست تگ‌ها |
| POST | `/api/tags/` | ایجاد تگ جدید |
| GET | `/api/tags/{id}/` | جزئیات یک تگ |
| PUT | `/api/tags/{id}/` | به‌روزرسانی کامل تگ |
| PATCH | `/api/tags/{id}/` | به‌روزرسانی جزئی تگ |
| DELETE | `/api/tags/{id}/` | حذف تگ |

### 5.3 FileTag ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/file-tags/` | لیست تگ‌های فایل‌ها |
| POST | `/api/file-tags/` | اختصاص تگ به فایل |
| GET | `/api/file-tags/{id}/` | جزئیات یک تگ فایل |
| PUT | `/api/file-tags/{id}/` | به‌روزرسانی کامل تگ فایل |
| PATCH | `/api/file-tags/{id}/` | به‌روزرسانی جزئی تگ فایل |
| DELETE | `/api/file-tags/{id}/` | حذف تگ از فایل |

**تحلیل Media App**: 18 endpoint که همگی CRUD استاندارد هستند

---

## 6. Gaming App Endpoints

### 6.1 Level ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/levels/` | لیست سطح‌ها |
| POST | `/api/levels/` | ایجاد سطح جدید |
| GET | `/api/levels/{id}/` | جزئیات یک سطح |
| PUT | `/api/levels/{id}/` | به‌روزرسانی کامل سطح |
| PATCH | `/api/levels/{id}/` | به‌روزرسانی جزئی سطح |
| DELETE | `/api/levels/{id}/` | حذف سطح |

### 6.2 UserLevel ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/user-levels/` | لیست سطح‌های کاربران |
| POST | `/api/user-levels/` | ثبت سطح کاربر |
| GET | `/api/user-levels/{id}/` | جزئیات یک سطح کاربر |
| PUT | `/api/user-levels/{id}/` | به‌روزرسانی کامل سطح کاربر |
| PATCH | `/api/user-levels/{id}/` | به‌روزرسانی جزئی سطح کاربر |
| DELETE | `/api/user-levels/{id}/` | حذف سطح کاربر |

### 6.3 Badge ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/badges/` | لیست نشان‌ها |
| POST | `/api/badges/` | ایجاد نشان جدید |
| GET | `/api/badges/{id}/` | جزئیات یک نشان |
| PUT | `/api/badges/{id}/` | به‌روزرسانی کامل نشان |
| PATCH | `/api/badges/{id}/` | به‌روزرسانی جزئی نشان |
| DELETE | `/api/badges/{id}/` | حذف نشان |

### 6.4 UserBadge ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/user-badges/` | لیست نشان‌های کاربران |
| POST | `/api/user-badges/` | اختصاص نشان به کاربر |
| GET | `/api/user-badges/{id}/` | جزئیات یک نشان کاربر |
| PUT | `/api/user-badges/{id}/` | به‌روزرسانی کامل نشان کاربر |
| PATCH | `/api/user-badges/{id}/` | به‌روزرسانی جزئی نشان کاربر |
| DELETE | `/api/user-badges/{id}/` | حذف نشان از کاربر |

### 6.5 UserPoint ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/user-points/` | لیست امتیازهای کاربران |
| POST | `/api/user-points/` | ثبت امتیاز کاربر |
| GET | `/api/user-points/{id}/` | جزئیات یک امتیاز کاربر |
| PUT | `/api/user-points/{id}/` | به‌روزرسانی کامل امتیاز کاربر |
| PATCH | `/api/user-points/{id}/` | به‌روزرسانی جزئی امتیاز کاربر |
| DELETE | `/api/user-points/{id}/` | حذف امتیاز کاربر |

### 6.6 UserAction ViewSet (6 endpoint)
| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/api/user-actions/` | لیست اقدامات کاربران |
| POST | `/api/user-actions/` | ثبت اقدام کاربر |
| GET | `/api/user-actions/{id}/` | جزئیات یک اقدام کاربر |
| PUT | `/api/user-actions/{id}/` | به‌روزرسانی کامل اقدام کاربر |
| PATCH | `/api/user-actions/{id}/` | به‌روزرسانی جزئی اقدام کاربر |
| DELETE | `/api/user-actions/{id}/` | حذف اقدام کاربر |

**تحلیل Gaming App**: 36 endpoint که همگی CRUD استاندارد هستند

---

## 7. Admin Panel

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/admin/` | پنل مدیریت Django |

---

## تحلیل Endpoint های مشابه

### گروه 1: CRUD استاندارد (138 endpoint)
همه ViewSet ها به صورت خودکار 6 endpoint استاندارد ایجاد می‌کنند:
- **GET** `/api/{resource}/` - لیست
- **POST** `/api/{resource}/` - ایجاد
- **GET** `/api/{resource}/{id}/` - دریافت جزئیات
- **PUT** `/api/{resource}/{id}/` - به‌روزرسانی کامل
- **PATCH** `/api/{resource}/{id}/` - به‌روزرسانی جزئی
- **DELETE** `/api/{resource}/{id}/` - حذف

**23 ViewSet × 6 endpoint = 138 endpoint مشابه**

### گروه 2: دریافت سوالات (3 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `GET /api/evaluations/{id}/questions/` | دریافت سوالات یک ارزیابی |
| `GET /api/quizzes/{id}/questions/` | دریافت سوالات یک کوئیز فعال |
| `GET /api/launch/{launch_id}/` | دریافت سوالات آزمون (integration) |

**3 endpoint که کار مشابه انجام می‌دهند (دریافت سوالات)**

### گروه 3: مدیریت کوئیز/آزمون (4 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `POST /api/quizzes/start/` | شروع کوئیز جدید |
| `POST /api/quizzes/submit/` | ارسال پاسخ‌های کوئیز |
| `POST /api/launch/{launch_id}/submit/` | ارسال پاسخ‌های آزمون (integration) |
| `POST /api/launch/{launch_id}/answer/` | ذخیره یک پاسخ (integration) |

**4 endpoint که کار مشابه انجام می‌دهند (مدیریت پاسخ‌های آزمون)**

### گروه 4: دریافت نتیجه (2 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `GET /api/quizzes/{id}/result/` | دریافت نتیجه نهایی کوئیز |
| `GET /api/launch/{launch_id}/redirect/` | ریدایرکت با نتیجه (integration) |

**2 endpoint که کار مشابه انجام می‌دهند (دریافت/نمایش نتیجه)**

### گروه 5: احراز هویت و Token (5 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `POST /api/login/` | لاگین با mobile و token |
| `POST /api/token/` | دریافت JWT token |
| `POST /api/token/refresh/` | تازه‌سازی token |
| `POST /api/token/verify/` | بررسی اعتبار token |
| `POST /api/token/logout/` | خروج از سیستم |

**5 endpoint که کار مشابه انجام می‌دهند (مدیریت احراز هویت)**

### گروه 6: ایجاد کاربر (2 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `POST /api/users/` | ایجاد کاربر (CRUD استاندارد) |
| `POST /api/users/create/` | ایجاد کاربر با صدور token (سفارشی) |

**2 endpoint که کار مشابه انجام می‌دهند (ایجاد کاربر)**

### گروه 7: Integration Exam Launch (2 endpoint)
| Endpoint | توضیحات |
|----------|---------|
| `GET /api/integration/exams/{eurl}/` | دریافت اطلاعات آزمون |
| `POST /api/integration/exams/launch/` | راه‌اندازی آزمون |

**2 endpoint که کار مشابه انجام می‌دهند (مدیریت launch آزمون برای integration)**

---

## خلاصه تحلیل

### تعداد Endpoint های مشابه:

1. **CRUD استاندارد**: 138 endpoint (همه ViewSet ها)
2. **دریافت سوالات**: 3 endpoint
3. **مدیریت پاسخ‌های آزمون**: 4 endpoint
4. **دریافت/نمایش نتیجه**: 2 endpoint
5. **احراز هویت و Token**: 5 endpoint
6. **ایجاد کاربر**: 2 endpoint
7. **Integration Exam Launch**: 2 endpoint

### پیشنهادات بهینه‌سازی:

1. **یکپارچه‌سازی endpoint های دریافت سوالات**: می‌توان یک endpoint واحد با پارامترهای مختلف ایجاد کرد
2. **یکپارچه‌سازی endpoint های مدیریت پاسخ**: endpoint های `/api/quizzes/submit/` و `/api/launch/{launch_id}/submit/` می‌توانند یکسان شوند
3. **یکپارچه‌سازی endpoint های احراز هویت**: `/api/login/` و `/api/token/` کار مشابه انجام می‌دهند
4. **حذف endpoint تکراری**: `/api/users/` و `/api/users/create/` می‌توانند یکی شوند

---

## آمار نهایی

- **کل endpoint ها**: 159
- **Endpoint های CRUD استاندارد**: 138
- **Endpoint های سفارشی**: 21
- **گروه‌های endpoint مشابه**: 7 گروه
- **بیشترین تکرار**: CRUD استاندارد (138 endpoint)

---

*تاریخ ایجاد: 2024*
*آخرین به‌روزرسانی: 2024*
