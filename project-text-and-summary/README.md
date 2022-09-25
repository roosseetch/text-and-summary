## Run backend on local machine

1. Install Poetry, follow the instructions: https://python-poetry.org/docs/#installation)
2. Start the Redis (as Celery brocker and backend ) and PosgresSQL DB in Docker containers `sh _assist/dev.sh db-redis up`
3. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
4. Run the DB migrations via poetry `poetry run python prestart.py` (only required once) (Unix users can use
the bash script if preferred `poetry run ./prestart.sh`)
5. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
6. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
7. Start the Celery worker in new terminal window `poetry run celery -A app.main.celery worker -l info --pool=prefork`
8. Open http://localhost:8001/
9. Open API documentation http://localhost:8001/docs or http://localhost:8001/redoc
10. Run the tests `poetry run pytest`
