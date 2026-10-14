# Semephu

Django + PostgreSQL project.

## Версии инструментов

| Инструмент      | Версия   |
| --------------- | -------- |
| Python          | 3.13.16  |
| Django          | 6.1.2    |
| psycopg         | 3.3.6    |
| python-dotenv   | 1.2.4    |
| PostgreSQL      | 17       |
| Docker          | 29.8.1   |
| Docker Compose  | 5.5.1    |

## Требования

- Python 3.13+
- Docker и Docker Compose (для базы данных)

## Запуск

1. Создайте и активируйте виртуальное окружение (если ещё не сделано):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` на основе примера:

   ```bash
   cp .env.example .env
   ```

   При необходимости измените значения. Переменные:

   | Переменная          | Назначение                       | Значение по умолчанию   |
   | ------------------- | -------------------------------- | ----------------------- |
   | `DJANGO_SECRET_KEY` | Секретный ключ Django            | insecure dev-ключ       |
   | `DJANGO_DEBUG`      | Режим отладки                    | `True`                  |
   | `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `localhost,127.0.0.1` |
   | `POSTGRES_DB`       | Имя базы данных                  | `semephu`               |
   | `POSTGRES_USER`     | Пользователь БД                  | `postgres`              |
   | `POSTGRES_PASSWORD` | Пароль БД                        | `postgres`              |
   | `POSTGRES_HOST`     | Хост БД                          | `localhost`             |
   | `POSTGRES_PORT`     | Порт БД                          | `5432`                  |

4. Поднимите базу данных PostgreSQL:

   ```bash
   docker compose up -d
   ```

5. Примените миграции:

   ```bash
   python manage.py migrate
   ```

6. (Опционально) Создайте суперпользователя для админки:

   ```bash
   python manage.py createsuperuser
   ```

7. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

Сайт будет доступен по адресу <http://127.0.0.1:8000/>, админка — <http://127.0.0.1:8000/admin/>.

## Полезные команды

```bash
docker compose ps        # статус контейнера с БД
docker compose down      # остановить БД
docker compose down -v   # остановить БД и удалить данные
python manage.py check   # проверка проекта
```

---

# Semephu

Django + PostgreSQL project.

## Tool versions

| Tool            | Version |
| --------------- | ------- |
| Python          | 3.13.16 |
| Django          | 6.1.2   |
| psycopg         | 3.3.6   |
| python-dotenv   | 1.2.4   |
| PostgreSQL      | 17      |
| Docker          | 29.8.1  |
| Docker Compose  | 5.5.1   |

## Requirements

- Python 3.13+
- Docker and Docker Compose (for the database)

## Getting started

1. Create and activate a virtual environment (if not done yet):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:

   ```bash
   cp .env.example .env
   ```

   Adjust values if needed. Variables:

   | Variable            | Purpose                          | Default                 |
   | ------------------- | -------------------------------- | ----------------------- |
   | `DJANGO_SECRET_KEY` | Django secret key                | insecure dev key        |
   | `DJANGO_DEBUG`      | Debug mode                       | `True`                  |
   | `DJANGO_ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
   | `POSTGRES_DB`       | Database name                    | `semephu`               |
   | `POSTGRES_USER`     | Database user                    | `postgres`              |
   | `POSTGRES_PASSWORD` | Database password                | `postgres`              |
   | `POSTGRES_HOST`     | Database host                    | `localhost`             |
   | `POSTGRES_PORT`     | Database port                    | `5432`                  |

4. Start the PostgreSQL database:

   ```bash
   docker compose up -d
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. (Optional) Create a superuser for the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

The site is available at <http://127.0.0.1:8000/>, the admin panel at <http://127.0.0.1:8000/admin/>.

## Useful commands

```bash
docker compose ps        # database container status
docker compose down      # stop the database
docker compose down -v   # stop the database and remove data
python manage.py check   # project checks
```
