from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.routers import router as visit_router
from app.config import settings


def create_app() -> FastAPI:
    """Create the application instance"""
    app = FastAPI(title=settings.SERVER_NAME)
    app.include_router(visit_router)

    @app.get("/")
    async def root():
        return RedirectResponse(url="/docs")

    return app
