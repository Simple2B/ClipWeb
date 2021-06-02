from datetime import datetime

import requests
from fastapi import HTTPException
from tortoise.query_utils import Q

from app.models import Visit
from app.serializers import Visit_Pydantic
from app.logger import log


async def check_clinicians_id(token: str or int, clinician_id: str or int) -> bool:
    """[Check if clinician with the id exist]"""
    headers = {{"Authorization": f"Bearer {token}"}}
    response = await requests.get(
        f"https://covid19-test.oth.io/clinician/api/clinicians/{clinician_id}",
        headers=headers,
    )
    if response.status_code != 200:
        log(log.WARNING, "Clinician with ID [%s] doesnt exist", clinician_id)
        return None
    return True


async def check_patients_id(token: str or int, pacient_id: str or int) -> bool:
    """[Check if pacient with the id exist]"""
    headers = {{"Authorization": f"Bearer {token}"}}
    response = await requests.get(
        f"https://covid19-test.oth.io/clinician/api/patients/{pacient_id}",
        headers=headers,
    )
    if response.status_code != 200:
        log(log.WARNING, "Patient with ID [%s] doesnt exist", pacient_id)
        return None
    return True


async def create_or_delete_visit(clinician_id: str or int, patient_id: str or int) -> bool:
    """[Check the data, after create or delete visit]"""
    visit = await Visit.filter(Q(clinicianId=clinician_id), Q(patientId=patient_id))
    if not visit:
        timestamp = int(datetime.now().timestamp())
        await Visit.create(
            clinicianId=clinician_id, patientId=patient_id, timestamp=timestamp
        )
        log(log.INFO("Visit has been created"))
        return True
    await visit[0].delete()
    log(log.INFO("Visit has been deleted"))
    return True


async def get_all_pacients_by_clinician(clinician_id: str or int) -> Visit_Pydantic:
    """[Get all IDs pacients by the clinician]"""
    pacients = []
    visits = await Visit.filter(clinicianId=clinician_id).order_by("timestamp")
    for visit in visits:
        pacients.append(visit.patientId)
    return pacients


async def check_data(
    clinician_id: str or int, pacient_id: str or int, token: str or int
):
    """[Check all data, raise exception if not validate]"""
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    check_patient = check_patients_id(token, pacient_id)
    if not check_patient:
        raise HTTPException(
            status_code=400,
            detail=f"Patient with id {pacient_id} does not exist",
        )
    check_clinician = check_clinicians_id(token, clinician_id)
    if not check_clinician:
        raise HTTPException(
            status_code=400,
            detail=f"Clinician with id {clinician_id} does not exist",
        )
