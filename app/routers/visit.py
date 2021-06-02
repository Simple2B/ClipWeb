from fastapi import APIRouter, Response

from app.services import (
    check_data,
    get_all_pacients_by_clinician,
    create_or_delete_visit,
)
from app.serializers import VisitIn_Pydantic

router = APIRouter(prefix="/clipweb")


@router.post("/visit")
async def setPinnedPatient(data: VisitIn_Pydantic, response: Response):
    token = response.headers["Authorization"]
    pacient_id = data["patientId"]
    clinician_id = data["clinicianId"]
    check_data(clinician_id, pacient_id, token)
    create_or_delete_visit(clinician_id, pacient_id)
    patients = get_all_pacients_by_clinician(clinician_id)
    return {"pinnedPatients": patients}
