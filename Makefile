migrate:
	docker compose run --rm backend python manage.py migrate

create_superuser:
	docker compose run --rm backend python manage.py add_superuser
