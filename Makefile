migrate:
	docker compose run --rm backend python manage.py migrate

create_superuser:
	docker compose run --rm backend python manage.py add_superuser

add_fake_data:
	docker compose run --rm backend python manage.py add_fake_data
