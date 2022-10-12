from fastapi import FastAPI
from uvicorn import run as startserver
from fastapi.middleware.cors import CORSMiddleware
from db import postgres_engine, redis_engine
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', status_code=200)
async def root():
    return {"status": "Working!", 'postgres': postgres_engine.__str__(), 'redis': redis_engine.__str__()}


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)

if __name__ == '__main__':
    startserver('main:app', host="0.0.0.0", port=8000, reload=True, reload_dirs=['/src'])
