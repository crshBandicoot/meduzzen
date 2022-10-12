from fastapi import FastAPI
from uvicorn import run as startserver
from db import postgres_engine, redis_engine
app = FastAPI()


@app.get('/', status_code=200)
async def root():
    return {"status": "Working!", 'postgres': postgres_engine.__str__(), 'redis':redis_engine.__str__()}


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)

if __name__ == '__main__':
    startserver(app, host="0.0.0.0", port=8000)
