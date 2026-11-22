## Запуск

```bash
cp .env.example .env          # заполнить DATABASE_URL и порт фронта в CORS_ORIGINS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# БД (один раз):
sudo -u postgres psql -c "CREATE ROLE kuda_user WITH LOGIN PASSWORD 'kuda_pass';"
sudo -u postgres psql -c "CREATE DATABASE kuda_post OWNER kuda_user;"

psql "$DATABASE_URL" -f schema.sql

uvicorn main:app --reload --port 8001


OpenAPI-схема: http://localhost:8001/openapi.json