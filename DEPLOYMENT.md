# План підготовки Django проєкту до розгортання на Render.com

**Мета:** Покроковий чеклист для підготовки будь-якого Django проєкту до production розгортання на Render.com з використанням Docker, Gunicorn та WhiteNoise.

---

## КРОК 1: Оновити requirements.txt

Встанови наступні залежності:
`pip install gunicorn`
`pip install whitenoise`

Онови requirements 
`pip freeze > requirements.txt`

Має додатись
```txt
gunicorn==23.0.0
whitenoise==6.8.2
python-dotenv==1.0.1
```
```

---

## КРОК 2: Налаштувати settings.py

### 2.1. Додати імпорти на початку файлу

Знайди рядок:
```python
from pathlib import Path
```

Заміни на:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
```

### 2.2. Налаштувати SECRET_KEY, DEBUG, ALLOWED_HOSTS

Знайди рядки:
```python
SECRET_KEY = 'ваш-секретний-ключ'
DEBUG = True
ALLOWED_HOSTS = []
```

Заміни на:
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'ваш-секретний-ключ-для-розробки')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
```

### 2.3. Додати WhiteNoise до MIDDLEWARE

Знайди список `MIDDLEWARE` і додай WhiteNoise **ПІСЛЯ** SecurityMiddleware:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- ДОДАЙ ЦЕЙ РЯДОК
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... решта middleware
]
```

### 2.4. Налаштувати статичні файли

Знайди секцію зі статичними файлами (зазвичай в кінці settings.py):
```python
STATIC_URL = 'static/'
```

Заміни/доповни на:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'  # Якщо проєкт в підпапці
# АБО
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Якщо manage.py в корені

STATICFILES_DIRS = [BASE_DIR / 'static']  # Якщо є окрема папка static

# WhiteNoise configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

## КРОК 3: Створити Dockerfile.prod

Створи новий файл `Dockerfile.prod` в корені проєкту:

```dockerfile
# Production Dockerfile for Render.com deployment
FROM python:3.14.2-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint-prod.sh

# Expose port
EXPOSE 8000

# Run entrypoint script
CMD ["/app/docker-entrypoint-prod.sh"]
```

**Команда:**
```bash
touch Dockerfile.prod
# Потім скопіюй вміст вище у файл
```

---

## КРОК 4: Створити docker-entrypoint-prod.sh

Створи файл `docker-entrypoint-prod.sh` в корені проєкту:

```bash
#!/usr/bin/env bash
set -e

echo "Starting production deployment..."

# Navigate to Django project directory (змінити якщо manage.py в іншій папці)
cd restaur  # <-- ЗМІНИТИ НА НАЗВУ ТВОЄЇ ПАПКИ З manage.py

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn server..."
exec gunicorn restaur.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

**ВАЖЛИВО:**
- Зміни `cd restaur` на назву папки де знаходиться manage.py
- Зміни `restaur.wsgi:application` на `<назва_проєкту>.wsgi:application`

**Команда:**
```bash
touch docker-entrypoint-prod.sh
chmod +x docker-entrypoint-prod.sh
# Потім скопіюй вміст вище у файл
```

---

## КРОК 5: Створити/оновити .dockerignore

Створи файл `.dockerignore` в корені проєкту:

```
# Git files
.git
.gitignore
.gitattributes

# Python cache
__pycache__
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Database
*.sqlite3
*.db

# Static and media files
staticfiles/
media/

# Environment variables
.env
.env.local
.env.*.local

# Docker files (production uses Dockerfile.prod)
docker-compose.yml

# Documentation
README.md
*.md
docs/

# Tests
tests/
test_*.py
*_test.py

# CI/CD
.github/
.gitlab-ci.yml

# Logs
*.log
logs/

# Node modules
node_modules/
npm-debug.log
```

**ВАЖЛИВО:**
- ⚠️ **НЕ додавай** `Dockerfile` та `docker-entrypoint.sh` в `.dockerignore`!
- Ці файли потрібні для локального запуску через docker-compose
- `.dockerignore` працює для ОБОХ Dockerfile (локального та production)
- Production використовує `Dockerfile.prod` та `docker-entrypoint-prod.sh`

**Команда:**
```bash
touch .dockerignore
# Потім скопіюй вміст вище у файл
```

---

## КРОК 6: Створити render.yaml

Створи файл `render.yaml` в корені проєкту:

```yaml
services:
  # Web Service
  - type: web
    name: your-app-name  # <-- ЗМІНИТИ НА НАЗВУ СВОГО ДОДАТКУ
    runtime: docker
    dockerfilePath: ./Dockerfile.prod
    region: frankfurt  # Можна змінити: oregon, singapore, frankfurt
    plan: free  # Або: starter, standard, pro
    branch: main  # Гілка для автоматичного розгортання
    healthCheckPath: /
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true  # Render згенерує автоматично
      - key: ALLOWED_HOSTS
        sync: false  # Встановиш вручну після розгортання
      - key: PYTHON_VERSION
        value: 3.14.2
      - key: PORT
        value: 8000
    autoDeploy: true  # Авто-деплой при push до main
```

**ВАЖЛИВО:** Зміни `your-app-name` на назву свого додатку

**Команда:**
```bash
touch render.yaml
# Потім скопіюй вміст вище у файл
```

---

## КРОК 7: Створити .env.example

Створи файл `.env.example` в корені проєкту:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1

# Database Configuration (optional для PostgreSQL)
# DATABASE_URL=postgresql://user:password@host:port/dbname

# Additional Settings
PYTHON_VERSION=3.14.2
PORT=8000
```

**Команда:**
```bash
touch .env.example
# Потім скопіюй вміст вище у файл
```

---

## КРОК 8: Згенерувати SECRET_KEY для production

**Варіант 1: Через Python**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Варіант 2: Онлайн**
- Перейди на https://djecrety.ir/
- Скопіюй згенерований ключ

**Збережи ключ** - він знадобиться для налаштування на Render!

---

## КРОК 8.5: Протестувати локальний Docker (РЕКОМЕНДОВАНО)

**Перед відправкою на GitHub, перевір що все працює локально!**

### Тест локального Dockerfile:

```bash
# 1. Зупини попередні контейнери (якщо є)
docker-compose down

# 2. Перебудуй та запусти контейнери
docker-compose up --build

# 3. Перевір що немає помилок:
# ✅ Контейнер запустився
# ✅ Міграції виконалися
# ✅ Сервер запущений на 0.0.0.0:8000

# 4. Відкрий http://localhost:8000 в браузері
# ✅ Сторінка завантажується
# ✅ Статичні файли працюють

# 5. Якщо все ОК, зупини контейнери
# Ctrl+C або в іншому терміналі:
docker-compose down
```

### Можливі помилки:

**Помилка:** `No such file or directory: docker-entrypoint.sh`
```bash
# Рішення:
# 1. Перевір що docker-entrypoint.sh НЕ в .dockerignore
# 2. Додай права на виконання:
chmod +x docker-entrypoint.sh
# 3. Перебудуй:
docker-compose up --build
```

**Помилка:** `Permission denied` для docker-entrypoint.sh
```bash
# Рішення:
chmod +x docker-entrypoint.sh
chmod +x docker-entrypoint-prod.sh
docker-compose up --build
```

---

## КРОК 9: Відправити код на GitHub

```bash
# 1. Перевір статус
git status

# 2. Додай всі файли
git add .

# 3. Створи коміт
git commit -m "Add production configuration for Render.com deployment"

# 4. Відправ на GitHub
git push origin main
```

**Якщо працюєш на іншій гілці:**
```bash
# Перейди на main
git checkout main

# Злий зміни з твоєї гілки (наприклад, deploy)
git merge deploy

# Відправ на GitHub
git push origin main
```

---

## КРОК 10: Зареєструватися на Render.com

1. Перейди на https://render.com
2. Натисни **"Get Started"** або **"Sign Up"**
3. Вибери **"Sign up with GitHub"** (рекомендовано)
4. Авторизуй Render доступ до твоїх репозиторіїв
5. Підтверди email (якщо потрібно)

---

## КРОК 11: Створити Web Service на Render

### Варіант 1: Через Blueprint (автоматично)

1. У Render Dashboard натисни **"New +"**
2. Вибери **"Blueprint"**
3. Вибери свій GitHub репозиторій
4. Render знайде файл `render.yaml` і покаже конфігурацію
5. Натисни **"Apply"**
6. Дочекайся завершення створення сервісу

### Варіант 2: Вручну

1. У Render Dashboard натисни **"New +"**
2. Вибери **"Web Service"**
3. Підключи GitHub репозиторій
4. Налаштуй:
   - **Name:** назва додатку
   - **Region:** Frankfurt (або інший)
   - **Branch:** main (або deploy, якщо деплоїш з іншої гілки)
   - **Runtime:** **Docker** (не Python!)
   - **Root Directory:** (залиш порожнім)
   - **Dockerfile Path:** `./Dockerfile.prod` ⚠️ **ВАЖЛИВО!**
     - Пиши ПОВНИЙ шлях: `./Dockerfile.prod`
     - НЕ просто `.` (крапка)
     - НЕ просто `Dockerfile.prod`
   - **Plan:** Free (або інший)
5. Натисни **"Create Web Service"**

**⚠️ Типові помилки:**
- ❌ Runtime: Python 3 → Має бути **Docker**
- ❌ Dockerfile Path: `.` → Має бути `./Dockerfile.prod`
- ❌ Заповнені Build Command та Start Command → Видали їх (не потрібні для Docker)

---

## КРОК 12: Налаштувати Environment Variables на Render

1. Перейди до свого сервісу на Render
2. Відкрий вкладку **"Environment"**
3. Натисни **"Add Environment Variable"**

**Додай наступні змінні:**

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (згенерований ключ з КРОКУ 8) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

**ВАЖЛИВО:** Заміни `your-app-name` на реальну назву свого додатку на Render

4. Натисни **"Save Changes"**
5. Render автоматично перезапустить сервіс

---

## КРОК 13: Дочекатися розгортання

1. Перейди на вкладку **"Logs"**
2. Спостерігай за процесом:
   ```
   Building Docker image...
   Installing dependencies...
   Running migrations...
   Collecting static files...
   Starting Gunicorn server...
   ```
3. Дочекайся статусу **"Live"** (зелений індикатор)

---

## КРОК 14: Перевірити додаток

1. Знайди URL додатку у верхній частині сторінки
   - Формат: `https://your-app-name.onrender.com`
2. Відкрий URL в браузері
3. Перевір:
   - ✅ Сторінка завантажується
   - ✅ Статичні файли (CSS/JS) працюють
   - ✅ Форми працюють
   - ✅ База даних працює (якщо є)

---

## ГОТОВО! 🚀

Твій Django додаток тепер запущений на Render.com!

---

## ДОДАТКОВО: Локальне тестування production конфігурації

### Тест з Docker:

```bash
# 1. Побудуй production image
docker build -f Dockerfile.prod -t my-app-prod .

# 2. Створи .env файл
cp .env.example .env
# Відредагуй .env (встанови SECRET_KEY, DEBUG=False, тощо)

# 3. Запусти контейнер
docker run -p 8000:8000 --env-file .env my-app-prod

# 4. Відкрий http://localhost:8000
```

### Тест без Docker:

```bash
# 1. Встанови залежності
pip install -r requirements.txt

# 2. Налаштуй .env
cp .env.example .env
# Відредагуй .env

# 3. Збери статичні файли і запусти
cd restaur  # Папка з manage.py
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn restaur.wsgi:application --bind 0.0.0.0:8000 --workers 3

# 4. Відкрий http://localhost:8000
```

---

## Troubleshooting (швидке вирішення проблем)

### Проблема: "DisallowedHost at /"
**Рішення:**
```
1. Перейди до Environment variables на Render
2. Онови ALLOWED_HOSTS: додай домен твого додатку
3. Приклад: your-app-name.onrender.com
4. Save Changes
```

### Проблема: Статичні файли не завантажуються
**Рішення:**
```bash
# Перевір у логах:
# python manage.py collectstatic --noinput

# Переконайся що в settings.py є:
# - STATIC_ROOT налаштований
# - WhiteNoise в MIDDLEWARE
# - STORAGES налаштований
```

### Проблема: 502 Bad Gateway
**Рішення:**
```
1. Перевір логи на Render (вкладка Logs)
2. Шукай помилки в міграціях або collectstatic
3. Перевір що SECRET_KEY встановлений
4. Перевір що PORT=8000
```

### Проблема: Application failed to respond
**Рішення:**
```bash
# Перевір docker-entrypoint-prod.sh:
# - Правильна назва папки в "cd папка"
# - Правильна назва проєкту в gunicorn команді
# - Файл має права на виконання (chmod +x)
```

### Проблема (локально): "No such file or directory: docker-entrypoint.sh"
**Рішення:**
```bash
# 1. Перевір .dockerignore - НЕ повинно бути:
#    - Dockerfile
#    - docker-entrypoint.sh

# 2. Додай права на виконання
chmod +x docker-entrypoint.sh

# 3. Перебудуй Docker
docker-compose down
docker-compose up --build
```

### Проблема (Render): "failed to read dockerfile: open Dockerfile.prod: no such file"
**Рішення:**
```bash
# 1. Перевір що файл існує локально
ls -la | grep Dockerfile.prod

# 2. Перевір що файл є на GitHub
# Перейди на https://github.com/username/repo
# Переключись на потрібну гілку (main/deploy)
# Перевір наявність Dockerfile.prod

# 3. Якщо файлу немає на GitHub - відправ його:
git add Dockerfile.prod docker-entrypoint-prod.sh
git commit -m "Add production Dockerfile"
git push origin deploy  # або main

# 4. У Render: Manual Deploy → Deploy latest commit
```

**Також перевір у Render:**
- Dockerfile Path має бути: `./Dockerfile.prod` (не просто `.`)
- Runtime має бути: Docker (не Python 3)

---

## Швидкий чеклист перед розгортанням

**Локальна підготовка:**
- [ ] `requirements.txt` містить gunicorn, whitenoise, python-dotenv
- [ ] `settings.py` налаштований (імпорти, SECRET_KEY, DEBUG, ALLOWED_HOSTS, WhiteNoise, STATIC_ROOT)
- [ ] `Dockerfile` та `Dockerfile.prod` створені
- [ ] `docker-entrypoint.sh` та `docker-entrypoint-prod.sh` створені і executable (chmod +x)
- [ ] `.dockerignore` НЕ містить Dockerfile та docker-entrypoint.sh (для локального запуску)
- [ ] `render.yaml` створений і налаштований
- [ ] `.env.example` створений
- [ ] SECRET_KEY згенерований

**Локальне тестування:**
- [ ] `docker-compose up --build` працює без помилок
- [ ] Сервер запускається на localhost:8000
- [ ] Статичні файли завантажуються локально

**Розгортання:**
- [ ] Усі файли відправлені на GitHub (перевір: Dockerfile.prod, docker-entrypoint-prod.sh, render.yaml)
- [ ] Гілка для деплою актуальна (main або deploy)
- [ ] Зареєстрований на Render.com
- [ ] Web Service створений
- [ ] Runtime обрано: **Docker** (не Python 3)
- [ ] Dockerfile Path: `./Dockerfile.prod` (не просто `.`)
- [ ] Environment variables налаштовані (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Додаток успішно задеплоєний на Render

---

## Швидка шпаргалка: Заповнення форми Render

**Коли створюєш Web Service вручну, заповнюй ТАК:**

```
✅ Name: variables-restaur (твоя назва)
✅ Project: My project / Production (опціонально)
✅ Language (Runtime): Docker
✅ Branch: deploy (або main)
✅ Region: Oregon/Frankfurt (будь-який)
✅ Root Directory: (ПОРОЖНЄ)
✅ Dockerfile Path: ./Dockerfile.prod

❌ Build Command: (ПОРОЖНЄ - видалити)
❌ Start Command: (ПОРОЖНЄ - видалити)
```

**Environment Variables:**
```
SECRET_KEY = [натисни Generate]
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
```

---

**Версія:** 2.2 (практичний чеклист + troubleshooting + Dockerfile Path)
**Дата:** 28.02.2026
**Оновлено:** Додано деталі про правильний Dockerfile Path та типові помилки
