from app.config.settings import settings
import pytest
import asyncio
from typing import Generator
from datetime import datetime
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app
# from app.models import ...

@pytest.fixture()
def client() -> Generator:
    app = create_app()
    initializer(["app.models"], "sqlite://:memory:")
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


# test user activation
def test_set_pinned_patient(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    # response = client.post(
    #     "/clipweb/set_pinned_patient/",
    #     json={
    #         ....
    #     },
    #     headers={"Authorization": f"Bearer {TEST_JWT_TOKEN}"},
    # )
    raise NotImplementedError()
