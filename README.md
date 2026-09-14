- Creating a new issue from command terminal, edit the "title" and "body" values
curl -i -X POST http://127.0.0.1:8000/issues -H "Content-Type: application/json" -d '{"title":"Issue number 2","body":"Testing Issue 2"}'


- Creating a new comment under an issue, edit the "body" field
curl -i -X POST http://127.0.0.1:8000/issues/3/comments -H "Content-Type:application/json" -d "{\"body\":\"This is a test comment on issue 2\"}"


