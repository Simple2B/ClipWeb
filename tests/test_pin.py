import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
import requests
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app
from app.services import (
    get_all_patients_by_clinician,
)
from .utils import create_few_visits


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


def test_get_all_patients(event_loop: asyncio.AbstractEventLoop):
    """Check func get_all_patients_by_clinician"""
    event_loop.run_until_complete(create_few_visits())
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert patients
    assert len(patients) == 2
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(4))
    assert not patients


def test_set_pinned_patient_positive(
    client: TestClient, event_loop: asyncio.AbstractEventLoop, monkeypatch
):
    """Check main route "/clipweb/pinnedPatients/{clinicianID}/{patientID}" """

    class MockResponse:
        ok = True

        @staticmethod
        def json():
            return {}

    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.post(
        "/clipweb/pinnedPatients/1/2",
        json={"pinUnpinFlag": True},
    )
    assert response.ok
    assert response.status_code == 200
    assert "pinnedPatients" in response.json()
    assert response.json()["pinnedPatients"]
    assert len(response.json()["pinnedPatients"]) == 1
    assert response.json()["pinnedPatients"][0]["uniqueId"] == 2
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert patients
    assert len(patients) == 1
    assert patients[0]["uniqueId"] == 2

    response = client.post(
        "/clipweb/pinnedPatients/1/2",
        json={"pinUnpinFlag": False},
    )
    assert response.ok
    assert response.status_code == 200
    assert "pinnedPatients" in response.json()
    assert not response.json()["pinnedPatients"]
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert not patients
