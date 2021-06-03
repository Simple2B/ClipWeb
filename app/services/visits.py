from datetime import datetime

import requests
from tortoise.query_utils import Q

from app.models import PatientPin
from app.logger import log


class ValidateException(Exception):
    def __init__(self, response_from_api: object, *args: object) -> None:
        super().__init__(*args)
        self.response_from_api = response_from_api

    @property
    def response(self):
        return self.response_from_api


def check_clinicians_id(headers: dict, clinician_id: str or int) -> None:
    """[Check if clinician with the id exist]"""
    response = requests.get(
        f"https://covid19-test.oth.io/clinician/api/clinicians/{clinician_id}",
        headers=headers,
    )
    if not response.ok:
        log(log.WARNING, "Clinician with ID [%s] doesn't exist", clinician_id)
        raise ValidateException(response)
    return response.json()


def check_patients_id(headers: dict, patient_id: str or int) -> None:
    """[Check if patient with the id exist]"""
    response = requests.get(
        f"https://covid19-test.oth.io/clinician/api/patients/{patient_id}",
        headers=headers,
    )
    if not response.ok:
        log(log.WARNING, "Patient with ID [%s] doesn't exist", patient_id)
        raise ValidateException(response)
    return response.json()


async def create_or_delete_visit(
    clinician_id: str or int, patient_id: str or int, pinflag: bool
) -> bool:
    """[Check the data, after create or delete visit]"""
    visit = await PatientPin.filter(
        Q(clinicianId=clinician_id), Q(patientId=patient_id)
    )
    if not visit and pinflag:
        timestamp = int(datetime.now().timestamp())
        await PatientPin.create(
            clinicianId=clinician_id, patientId=patient_id, timestamp=timestamp
        )
        log(log.INFO, "Visit has been created")
        return True
    elif visit and not pinflag:
        for each in visit:
            await each.delete()
        log(log.INFO, "Visit(s) has been deleted")
    return True


async def get_all_patients_by_clinician(clinician_id: str or int):
    """[Get all IDs patients by the clinician]"""
    patients = []
    visits = await PatientPin.filter(clinicianId=clinician_id).order_by("timestamp")
    for visit in visits:
        patients.append(visit.patientId)
    return patients
