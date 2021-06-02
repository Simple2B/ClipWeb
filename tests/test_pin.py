import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app
from app.services import (
    get_all_pacients_by_clinician,
)
from .utils import create_few_visits

# from app.models import ...

TOKEN = "4567*GFYsbaUFN(Sygfasvtdyabs"


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


def test_get_all_pacients(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    event_loop.run_until_complete(create_few_visits())
    pacients = event_loop.run_until_complete(get_all_pacients_by_clinician(1))
    assert pacients
    assert len(pacients) == 2
    pacients = event_loop.run_until_complete(get_all_pacients_by_clinician(4))
    assert not pacients


# test user activation
# def test_set_pinned_patient(client: TestClient, event_loop: asyncio.AbstractEventLoop):
# response = client.post(
#     "/clipweb/set_pinned_patient/",
#     json={
#         ....
#     },
#     headers={"Authorization": f"Bearer {TEST_JWT_TOKEN}"},
# )
# pass


# def test_check_clinician_id(client: TestClient, event_loop: asyncio.AbstractEventLoop):
#     check_clinician = check_clinicians_id(TOKEN, 1)
#     assert check_clinician


# def test_check_patient_id(client: TestClient, event_loop: asyncio.AbstractEventLoop):
#     check_patient = check_patients_id(TOKEN, 1)
#     assert check_patient


# def test_check_visit(client: TestClient, event_loop: asyncio.AbstractEventLoop):
#     checkvisit = check_visit(1, 1)
#     assert checkvisit


# def test_create_or_delete_visit(client: TestClient, event_loop: asyncio.AbstractEventLoop):
#     event_loop.run_until_complete()
#     pass
