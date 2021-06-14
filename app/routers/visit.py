from fastapi import APIRouter, HTTPException

from app.services import (
    get_all_patients_by_clinician,
    create_or_delete_visit,
    ValidateException,
)
from app.serializers import CheckPatientPin, CheckPatientPinResponse
from app.logger import log

router = APIRouter(prefix="/clipweb")


@router.post(
    "/pinnedPatients/{clinician_id}/{patient_id}",
    response_model=CheckPatientPinResponse,
)
async def setPinnedPatient(data: CheckPatientPin, clinician_id: str, patient_id: str):
    """[Main method]

    Args:
        data (CheckPatientPin): [Flag for create/delete pin]
        clinician_id (str): [ID]
        patient_id (str): [ID]

    Raises:
        HTTPException: []

    Returns:
        [JSON]: [All patients IDs by clinician ID]
    """
    pin_flag = data.pinUnpinFlag
    try:
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
