from fastapi.middleware.cors import CORSMiddleware


def add_middleware(app):
    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
