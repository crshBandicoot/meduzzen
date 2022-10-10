from fastapi import FastAPI

app = FastAPI()


@app.get('/', status_code=200)
async def root():
    return {"status": "Working"}


def health_check():
    return 200


app.add_api_route('/health', endpoint=health_check)
