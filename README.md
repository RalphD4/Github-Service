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
  -d '{"title":"[ISSUE TITLE]","body":"[ISSUE DETAIL]"}'
```

List your issues:
```bash
curl -i http://127.0.0.1:8000/issues
```

Update your issues:
```bash
curl -i -X PATCH http://127.0.0.1:8000/issues/3 \
  -H "Content-Type: application/json" \
  -d '{"state":"[ISSUE CLOSED]"}'
```

Add comments:
```bash
curl -i -X POST http://127.0.0.1:8000/issues/3/comments \
  -H "Content-Type: application/json" \
  -d '{"body":"[ISSUE COMMENT]"}'
```

Health check:
```bash
curl -i http://127.0.0.1:8000/healthz
```

## Webhooks

To register the webhook, do so via Settings, then Webhooks.

## Design Note

### Error mapping

The service keeps client errors distinct from errors returned by GitHub. Request validation is performed before making an upstream call: malformed JSON fields, missing required fields, invalid issue state, and empty updates return `400 Bad Request`. A missing issue is mapped to `404 Not Found`. GitHub authentication failures are returned as `401`, while other GitHub response statuses are preserved so callers can distinguish authorization, validation, and server failures. GitHub rate-limit responses should be exposed as `429 Too Many Requests` with `Retry-After`; the existing rate-limit helper derives this from `Retry-After` or `X-RateLimit-Reset`.

Error bodies use a small JSON shape such as `{"error": "Invalid payload"}`. A production version should normalize this to the OpenAPI `error`/`message`/`details` schema and avoid returning raw upstream response bodies, which may expose implementation details. Timeouts and connection failures should be mapped to `502 Bad Gateway` (or `504 Gateway Timeout`) rather than being reported as successful requests.

### Pagination strategy

`GET /issues` uses GitHub's page-number pagination. The API accepts `page` (default `1`) and `per_page` (default `30`), and forwards both values to GitHub. The documented maximum is `100`; clients should request pages until a response contains fewer than `per_page` items. This keeps the service stateless and avoids loading the entire repository into memory, at the cost of an extra request per page and possible changes between pages while issues are created or closed. A future response envelope could include `page`, `per_page`, and `has_next` metadata, but the current array response preserves a simple compatibility surface.

### Webhook deduplication

GitHub's `X-GitHub-Delivery` value is the idempotency key. After validating the HMAC signature and event shape, the service inserts the delivery ID into SQLite, where it is the primary key. Repeated deliveries therefore produce one stored event and still receive `204`, making retries safe for the current logging-only handler. The insert is committed before the response is sent.

This is intentionally at-least-once delivery with idempotent storage, not a distributed queue. The SQLite database is local to the container, so dedupe state is lost when ephemeral storage is replaced and is not shared across replicas. A multi-instance deployment should use a durable shared store with an atomic insert, and side effects should be recorded or processed transactionally with the dedupe claim.

### Security trade-offs

The GitHub token remains in environment configuration and is sent only from the service to GitHub; it is not accepted from clients. Webhooks use `X-Hub-Signature-256`, HMAC-SHA256, and constant-time comparison over the raw request body, which protects integrity and authenticates the configured sender. The delivery ID prevents ordinary retries from creating duplicate records.

The current deployment still has important trade-offs. The OpenAPI document declares bearer authentication for issue endpoints, but the Flask routes do not yet enforce it, and `CORS(app)` permits all origins. Those defaults are convenient for a classroom/demo deployment but allow unauthenticated issue operations and broaden browser access. Before production, enforce bearer-token validation at the application boundary, restrict CORS to trusted origins, run behind HTTPS, use a least-privilege GitHub token, and keep secrets out of images and logs. Webhook replay protection should also include a durable delivery store and, where required, an age policy; signature verification alone proves authenticity but does not prove freshness.
