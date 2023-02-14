build:
	docker compose build
migrations:
	docker compose run --rm app sh -c "python manage.py wait_for_db && \
		python manage.py makemigrations"
superuser:
	docker compose run --rm app sh -c "python manage.py createsuperuser"
run:
	docker compose up
lint:
	docker compose run --rm app sh -c "flake8"
