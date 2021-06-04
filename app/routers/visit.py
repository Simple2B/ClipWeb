from fastapi import APIRouter, Request, HTTPException

from app.services import (
    get_all_patients_by_clinician,
    create_or_delete_visit,
    check_clinicians_id,
    check_patients_id,
    ValidateException,
)
from app.serializers import CheckPatientPin, CheckPatientPinResponse
from app.logger import log

router = APIRouter(prefix="/clipweb")


@router.post(
    "/pinnedPatients/{clinician_id}/{patient_id}",
    response_model=CheckPatientPinResponse,
)
async def setPinnedPatient(
    data: CheckPatientPin, request: Request, clinician_id: int, patient_id: int
):
    headers = {"Authorization": dict(request.headers)["authorization"]}
    pin_flag = data.pinUnpinFlag
    try:
        check_patients_id(headers, patient_id)
        check_clinicians_id(headers, clinician_id)
        await create_or_delete_visit(clinician_id, patient_id, pin_flag)
        patients = await get_all_patients_by_clinician(clinician_id)
        return {"pinnedPatients": patients}
    except ValidateException as e:
        log(
            log.WARNING,
            "Response from 3rd party service is [%s]",
            e.response.status_code,
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json() if e.response.text else e.response.reason,
        )
