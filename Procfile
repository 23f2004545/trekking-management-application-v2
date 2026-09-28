web: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
worker: celery -A tasks.celery_app worker --workdir backend --loglevel=info --concurrency=2
beat: celery -A tasks.celery_app beat --workdir backend --loglevel=info
