docker build -t flask-mdad:latest .
docker compose up -d (debug mode, uses docker-compose.yml and docker-compose.override.yml)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d (production mode)
docker compose exec web python init_db.py

Migrating the database:

docker compose exec web flask db init
docker compose exec web flask db migrate -m "xyz"
docker compose exec web flask db upgrade

DB backup and restore:

docker compose exec db pg_dump --clean --if-exists -U flaskuser -d flaskdb > dump.sql
cat dump.sql | docker compose exec -T db psql -U flaskuser -d flaskdb
