# IndiLearn Vocabulary API

IndiLearn Vocabulary is a FastAPI backend for an English vocabulary training application. It stores users, vocabulary items, ranks, achievements, and answer history in PostgreSQL. Item selection uses an Item Response Theory (IRT) model for users outside the control group.

## What Is Included

- FastAPI application with interactive OpenAPI documentation
- HTTP Basic authentication backed by an Apache `htpasswd` file
- Vocabulary item retrieval and answer checking
- Score and rank updates after submitted answers
- Achievement detection and user achievement history
- Top-10 leaderboard
- PostgreSQL persistence through SQLAlchemy
- Docker images for the API and database backup service

The repository contains the backend only. It does not contain a frontend, production secrets, the `htpasswd` file, or the complete runtime CSV dataset.

## API

The API listens on port `8000` in the Docker setup. Once it is running:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

Routes currently exposed by the application:

| Method | Path | Authentication | Purpose |
| --- | --- | --- | --- |
| `GET` | `/user/get` | Basic auth | Get the authenticated user |
| `GET` | `/user/achievements/check` | Basic auth | Check and award newly unlocked achievements |
| `GET` | `/user/achievements/get` | Basic auth | Get the authenticated user's achievement IDs |
| `GET` | `/item/get` | Basic auth | Get the next vocabulary item |
| `POST` | `/item/check` | Basic auth | Check an answer and update score/rank |
| `GET` | `/achievement/get/{achievement_id}` | Public | Get one achievement |
| `GET` | `/achievement/get_all` | Public | Get all achievements |
| `GET` | `/leaderboard/get` | Public | Get the top users |
| `GET` | `/rank/get/{rank_id}` | Public | Get a rank |
| `GET` | `/rank/get_current` | Basic auth | Get the authenticated user's rank |

The answer endpoint expects JSON containing `item_id` and `user_solution`, for example:

```json
{
	"item_id": 1,
	"user_solution": "answer"
}
```

## Docker Deployment

Docker Compose uses prebuilt images by default:

- `indilearn-api:latest`
- `indilearn-db:latest`

It does not build those images automatically. Build them locally with:

```bash
docker build -t indilearn-api:latest -f Dockerfile.api .
docker build -t indilearn-db:latest -f Dockerfile.db .
```

Before starting the stack, provide these files in the repository root:

- `.env`, mounted into the API container as `/mnt/.env`
- `.htpasswd`, mounted into the API container as `/mnt/.htpasswd`
- `.env_db`, mounted into the database container as `/mnt/.env`
- Runtime data under `data/`, mounted into the API container as `/mnt/data/`

The Compose configuration uses these variables:

| Variable | Used for |
| --- | --- |
| `DATABASE_URL` | API SQLAlchemy connection string |
| `PG_USER` | PostgreSQL user |
| `PG_NAME` | PostgreSQL database name |
| `PG_PASSWORD` | PostgreSQL password |
| `API_IMAGE` | Optional API image override |
| `DB_IMAGE` | Optional database image override |

Start the stack after building the images and supplying the configuration files:

```bash
docker compose up -d
```

The database uses a named Docker volume, `postgres_data`. To stop the stack while preserving data:

```bash
docker compose down
```

To remove the database volume as well, use `docker compose down -v`. This deletes the stored database data.

## Local Development

The project targets Python 3.10. The API also requires a reachable PostgreSQL database and the runtime configuration/data files described above.

Create an environment and install dependencies:

```bash
python3.10 -m venv .py_env
source .py_env/bin/activate
python -m pip install -r requirements.txt
```

Run the API from the repository root:

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

The same development server can also be started through the application's entry point:

```bash
python api/main.py
```

On Windows, activate the environment with `.py_env\Scripts\Activate.ps1` first. The `python api/main.py` command and the Uvicorn command above both start the API with reload enabled.

## Code Quality

Formatting and lint configuration is in `pyproject.toml`. The checks used by GitHub Actions are:

```bash
python -m black --check .
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 . --count --exit-zero --statistics
python -m autoflake --check --recursive .
```

GitHub Actions runs these checks on pushes and pull requests using Python 3.10. It currently does not run `pytest` or build Docker images.

## Tests

Tests are located under `api/tests`. The test configuration expects PostgreSQL through `TEST_DATABASE_URL`; authentication defaults to `test-user` and `test-password`, and can be overridden with `TEST_AUTH_USERNAME` and `TEST_AUTH_PASSWORD`.

Run the configured test command with:

```bash
python -m pytest
```

The test suite is not currently part of the GitHub Actions workflow. Some older achievement tests are incomplete or disabled, and the current pytest path/data configuration requires cleanup before the complete suite can be treated as a reliable CI gate.

## Repository Scripts

- `build_and_push.sh`: builds and pushes API and database images to GitHub Container Registry; requires the GitHub Container Registry variables used in the script.
- `backup.sh`: creates a PostgreSQL dump from inside the database container.
- `restart_server.sh` and `scripts/restart_server.sh`: pull images and restart the Compose deployment.
- `scripts/style.sh`: applies Black and Autoflake, then runs style checks using the local `.py_env` environment.

## Related Documentation

- [Contributing](CONTRIBUTING.md)
