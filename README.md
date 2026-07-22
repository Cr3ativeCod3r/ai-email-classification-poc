# AI Message Router (PoC)

Microservice-based intelligent message routing system using Python, FastAPI, Ollama (`llama3.2`), and MailHog.

## Architecture

The project is split into the following microservices:
- **router-service (FastAPI)**: Exposes the main `POST /api/v1/messages` endpoint. Uses `pydantic-ai` with local Ollama model to route messages based on reasoning. Sends an HTTP request to `notification-service` to dispatch the email.
- **notification-service (FastAPI)**: Internal service with `POST /internal/v1/emails`. Responsible for SMTP communication with MailHog.
- **ollama**: Runs the LLM engine and automatically downloads the model upon startup using an initialization service (`init-ollama`).
- **mailhog**: SMTP server and UI to intercept and display sent emails.

## Prerequisites

- Docker and Docker Compose (Compose v2)

## Setup and Running

1. Ensure Docker is running.
2. In the root directory, start the stack:
   ```bash
   docker compose up -d
   ```
   *Note: On the first run, the `init-ollama` container will download the `llama3.2` model. The `router-service` will only start after Ollama is healthy and `init-ollama` completes.*

3. The services will be available at:
   - **Router Service API**: `http://localhost:8000`
   - **OpenAPI Swagger Docs**: `http://localhost:8000/api/v1/docs`
   - **MailHog UI**: `http://localhost:8025`

## Example Usage

You can test the system via the Swagger UI (`http://localhost:8000/api/v1/docs`) or using `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/messages' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user.test@example.com",
  "message": "My computer monitor is broken and I cannot work."
}'
```

After executing the request, check the MailHog UI at `http://localhost:8025` to see the captured email addressed to `it@example.com` (or similar depending on LLM decision) with the `Reply-To` set to `user.test@example.com`.

## Development

The project uses `uv` for dependency management. Each microservice contains its own `pyproject.toml` and `uv.lock`.

To run tests locally:
```bash
cd router-service
PYTHONPATH=src uv run pytest

cd ../notification-service
PYTHONPATH=src uv run pytest
```
