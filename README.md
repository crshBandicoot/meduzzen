To create DB migrations:
    alembic revision --autogenerate -m 'init'
Start app by executing:
    uvicorn src.main:app --reload
Docker:
    docker compose -f 'compose.yml' up --build -d
Run tests:
    docker compose -f 'compose.tests.yml' up --build --abort-on-container-exit