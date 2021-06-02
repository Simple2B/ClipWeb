from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import router as visit_router


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI()
    app.include_router(visit_router)


    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    add_pagination(app)
    return app
