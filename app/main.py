from os import getcwd, getenv
from fastapi import FastAPI
from uvicorn import run as startserver
from config import configure


app = FastAPI()
configure(app)


@app.get('/', status_code=200)
async def root():
    return {"status": "Working!"}


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)

if __name__ == '__main__':
    startserver('main:app', host="0.0.0.0", port=int(getenv('APP_PORT')), reload=True, reload_dirs=[getcwd()])
