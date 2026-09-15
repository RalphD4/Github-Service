# Github-Service

## Setup

To run locally, go to the root of the directory then run pip install -r requirements.txt, set env vars, python -m backend.app.

To run on Docker, run docker build -t github-service . then docker run --env-file .env -p 8000:8000 github-service.

You need the following ENV VARS GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, WEBHOOK_SECRET, PORT. Your personal access token should have permissions to read and write on the target repository.

## API examples

To create an issue, do this:
```bash
curl -i -X POST http://127.0.0.1:8000/issues \
  -H "Content-Type: application/json" \
  -d '{"title":"Watch Tower Issue","body":"No light"}'
```

List your issues:
```bash
curl -i http://127.0.0.1:8000/issues
```

Update your issues:
```bash
curl -i -X PATCH http://127.0.0.1:8000/issues/3 \
  -H "Content-Type: application/json" \
  -d '{"state":"closed"}'
```

Add comments:
```bash
curl -i -X POST http://127.0.0.1:8000/issues/3/comments \
  -H "Content-Type: application/json" \
  -d '{"body":"fill in later"}'
```

Health check:
```bash
curl -i http://127.0.0.1:8000/healthz
```

## Webhooks

To register the webhook, do so via Settings, then Webhooks.
