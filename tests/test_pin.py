import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
import requests
from requests.auth import HTTPBasicAuth
from tortoise.contrib.test import finalizer, initializer

from app.setup import create_app
from app.services import (
    get_all_patients_by_clinician,
    check_clinicians_id,
    check_patients_id,
)
from .utils import create_few_visits
from app.config import settings

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


def test_get_all_patients(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    event_loop.run_until_complete(create_few_visits())
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert patients
    assert len(patients) == 2
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(4))
    assert not patients


@pytest.mark.skipif(not settings.USERNAME, reason="OTH USERNAME not configured")
def test_set_pinned_patient_negative(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
):
    auth = HTTPBasicAuth(settings.USERNAME, settings.PASSWORD)
    response = requests.get("https://covid19-test.oth.io/idp2/users/auth", auth=auth)
    headers = {"Authorization": f"Bearer {response.json()['token']}"}
    clinician_id = 1
    check_clinicians_id(headers, clinician_id)
    res = requests.get(
        "https://covid19-test.oth.io/clinician/api/patients", headers=headers
    )
    assert res.ok
    patient_url = res.json()["results"][0]["links"]["patient"]
    patient_id = int(patient_url.split("/")[-1])
    check_patients_id(headers, patient_id)
    response = client.post(
        "/clipweb/pinnedPatients",
        json={
            "clinicianId": clinician_id,
            "patientId": patient_id,
            "pinUnpinFlag": True,
        },
        headers=headers,
    )
    assert response.ok
    assert response.status_code < 300


def test_set_pinned_patient_positive(
    client: TestClient, event_loop: asyncio.AbstractEventLoop, monkeypatch
):
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
        "/clipweb/pinnedPatients",
        json={"clinicianId": 1, "patientId": 2, "pinUnpinFlag": True},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    assert response.ok
    assert response.status_code == 200
    assert "pinnedPatients" in response.json()
    assert response.json()["pinnedPatients"]
    assert len(response.json()["pinnedPatients"]) == 1
    assert response.json()["pinnedPatients"][0] == 2
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert patients
    assert len(patients) == 1
    assert patients[0] == 2

    response = client.post(
        "/clipweb/pinnedPatients",
        json={"clinicianId": 1, "patientId": 2, "pinUnpinFlag": False},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    assert response.ok
    assert response.status_code == 200
    assert "pinnedPatients" in response.json()
    assert not response.json()["pinnedPatients"]
    patients = event_loop.run_until_complete(get_all_patients_by_clinician(1))
    assert not patients
