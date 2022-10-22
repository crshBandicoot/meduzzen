To create DB migrations:
    sudo alembic revision --autogenerate -m 'init'
Start app by executing:
    uvicorn src.main:app --reload
Docker:
    sudo sudo docker-compose up --build -d