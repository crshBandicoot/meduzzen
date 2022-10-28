To create DB migrations:
    alembic revision --autogenerate -m 'init'
Start app by executing:
    uvicorn src.main:app --reload
Docker:
   docker-compose up --build -d