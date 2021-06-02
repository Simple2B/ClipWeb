from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import auth_router, gate_router, client_router


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(gate_router)
    app.include_router(client_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    add_pagination(app)
    return app
