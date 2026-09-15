- How to run locally (Docker/Non-Docker)
...


- Env var setup and scopes used
GITHUB_TOKEN = "......."
GITHUB_OWNER = RalphD4
GITHUB_REPO = Github-Service
WEBHOOK_SECRET = shared_webhook_secret


- API examples:
- List of current issues (there should be x amount)
http://127.0.0.1:8000/issues

- Create a new issue from cmd with curl, edit the "title" and "body" as needed
curl -i -X POST http://127.0.0.1:8000/issues -H "Content-Type: application/json" -d '{"title":"Watch Tower Issue","body":"No light"}'

- Create a new comment under an existing issue, edit the "body" field as needed
curl -i -X POST http://127.0.0.1:8000/issues/3/comments -H "Content-Type:application/json" -d "{\"body\":\"fill in later\"}"

- Updating an issue
curl -i -X PATCH http://127.0.0.1:8000/issues/2 -H "Content-Type: application/json" -d "{\"body\":\"This is the updated body\"}"


- healthz
http://127.0.0.1:8000/healthz



- Webhook setup steps and redelivery instructions
...

- 

