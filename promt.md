You are an expert Django developer building a backend API for a gamification system. The system is API-only (no frontend), multi-tenant (using companyId for isolation), and focuses on security for organizational clients. Use Django 4+ with Django REST Framework (DRF) for the APIs. Database is PostgreSQL with schemas: roadmap, users, exam, media.

First, create a new Django project named "kebrit_api" with `source .env/bin/activate` active env. Then, create separate apps for each schema: "roadmap_app", "users_app", "exam_app", "media_app".

Define models in each app exactly matching this SQL schema (use Django ORM, set db_table and schema in Meta class, e.g., class Meta: db_table = 'mission'; managed = False if needed, but prefer managed=True for migrations). Include all fields, relationships, and constraints as specified. Use ForeignKey with on_delete=CASCADE where applicable.

Here is the full SQL schema:

-- Schemas
CREATE SCHEMA roadmap;
CREATE SCHEMA users;
CREATE SCHEMA exam;
CREATE SCHEMA media;

-- Roadmap tables
CREATE TABLE roadmap.mission (
    id SERIAL PRIMARY KEY,
    companyId INTEGER,
    userId INTEGER,
    type CHAR(1),
    title VARCHAR(255),
    content TEXT,
    mo BOOLEAN,
    point INTEGER,
    createAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modifiedAt TIMESTAMP,
    expierAt TIMESTAMP,
    isActive BOOLEAN DEFAULT TRUE,
    atLeastPoint INTEGER
);
CREATE TABLE roadmap.missionRelation (
    id SERIAL PRIMARY KEY,
    missionId INTEGER,
    parentId INTEGER,
    childId INTEGER
);
CREATE TABLE roadmap.missionResult (
    id SERIAL PRIMARY KEY,
    missionId INTEGER,
    userId INTEGER,
    state VARCHAR(50),
    userGrant INTEGER,
    quizId INTEGER,
    abilityId INTEGER
);
CREATE TABLE roadmap.ability (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    companyId INTEGER
);

-- Users tables
CREATE TABLE users.company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE users.user (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255),
    companyId INTEGER,
    mobile VARCHAR(20),
    name VARCHAR(100),
    password VARCHAR(255)
);
CREATE TABLE users.session (
    uuid UUID PRIMARY KEY,
    userId INTEGER,
    expierAt TIMESTAMP
);
CREATE TABLE users.token (
    uuid UUID PRIMARY KEY,
    userId INTEGER
);
CREATE TABLE users.role (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    companyId INTEGER
);
CREATE TABLE users.userRole (
    id SERIAL PRIMARY KEY,
    userId INTEGER,
    roleId INTEGER
);

-- Exam tables
CREATE TABLE exam.evaluation (
    id SERIAL PRIMARY KEY,
    type BOOLEAN,
    acceptScore INTEGER,
    numberOfQuestion INTEGER,
    missionId INTEGER,
    userId INTEGER,
    createAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    isActive BOOLEAN DEFAULT TRUE,
    canBack BOOLEAN DEFAULT TRUE,
    duration INTEGER
);
CREATE TABLE exam.question (
    id SERIAL PRIMARY KEY,
    evaluationId INTEGER,
    description TEXT,
    img VARCHAR(255),
    type BOOLEAN,
    c1 TEXT,
    c2 TEXT,
    c3 TEXT,
    c4 TEXT,
    correct INTEGER,
    answer TEXT,
    weight FLOAT,
    canShuffle BOOLEAN DEFAULT FALSE
);
CREATE TABLE exam.quiz (
    id SERIAL PRIMARY KEY,
    evaluationId INTEGER,
    userId INTEGER,
    startAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    endAt TIMESTAMP,
    score FLOAT,
    isAccept BOOLEAN,
    state VARCHAR(50)
);
CREATE TABLE exam.quizResponse (
    id SERIAL PRIMARY KEY,
    quizId INTEGER,
    questionId INTEGER,
    answer INTEGER,
    score FLOAT,
    done VARCHAR(255)
);
CREATE TABLE exam.quizResponseEvaluation (
    id SERIAL PRIMARY KEY,
    userId INTEGER,
    quizResponseId INTEGER,
    score FLOAT
);

-- Media tables
CREATE TABLE media.file (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid() UNIQUE,
    userId INTEGER,
    companyId INTEGER,
    productId INTEGER,
    fileName VARCHAR(255),
    fileType VARCHAR(50),
    fileSize BIGINT,
    path TEXT NOT NULL,
    bucket VARCHAR(255),
    url TEXT,
    isPublic BOOLEAN DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE media.tag (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);
CREATE TABLE media.fileTag (
    fileId INTEGER REFERENCES media.file(id) ON DELETE CASCADE,
    tagId INTEGER REFERENCES media.tag(id) ON DELETE CASCADE,
    PRIMARY KEY (fileId, tagId)
);

-- Foreign Keys (implement in models with ForeignKey)
-- (Include all ALTER TABLE ADD CONSTRAINT statements from the original schema here, but map to ORM)

-- Indexes (add via Meta: indexes = [models.Index(fields=['companyId'], name='idx_mission_companyId'), etc.]

For Phase 1: Implement only basic CRUD APIs (Create, Read, Update, Delete) for ALL models. No advanced logic like quiz scoring, mission expiration checks, or file uploads yet—focus solely on reading/writing data to/from the DB.

Use DRF: For each model, create a Serializer (ModelSerializer), a ViewSet (ModelViewSet with queryset=Model.objects.all(), serializer_class=YourSerializer), and register in urls.py with routers (e.g., DefaultRouter).

Security:
- Use JWT authentication (install djangorestframework-simplejwt).
- Custom permissions: Ensure users can only access data where companyId matches their own company (via request.user.companyId). Use DRF permissions (e.g., class CompanyPermission(BasePermission)) and add to permission_classes.
- Role-based access: For admin roles, allow broader access; otherwise, restrict to user's own data.
- Rate limiting: Install django-ratelimit and apply to views.
- No CSRF for APIs, but enable CORS (install django-cors-headers).

Project structure:
- settings.py: Add apps, DRF settings (DEFAULT_AUTHENTICATION_CLASSES = ['rest_framework_simplejwt.authentication.JWTAuthentication']), database config for PostgreSQL with schemas.
- urls.py: Include router.urls for each app (e.g., router.register(r'missions', MissionViewSet)).
- For media.file: Handle uuid with UUIDField(default=uuid.uuid4), but no file upload logic yet—just CRUD on metadata.

Generate initial migrations, but assume DB schema exists (use managed=False if needed for existing tables).

Output the full code structure: All models.py, serializers.py, views.py, urls.py, settings.py updates, and any custom permissions.py. Make it ready to run with python manage.py makemigrations && migrate && runserver.

Expected scale: Up to 100 concurrent users/second, so optimize querysets if needed (e.g., select_related for FKs).