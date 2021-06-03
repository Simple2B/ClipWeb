from datetime import datetime
from app.models import PatientPin


async def create_test_visit(
    clinician_id: int = 1,
    patient_id: int = 1,
    timestamp: int = datetime.timestamp(datetime.now()),
) -> PatientPin():

    test_patient_pin = await PatientPin.create(
        clinicianId=clinician_id,
        patientId=patient_id,
        timestamp=timestamp,
    )

    return test_patient_pin


async def create_few_visits():
    for i in range(3):
        await create_test_visit(clinician_id=i, patient_id=i)
        await create_test_visit(clinician_id=i, patient_id=i + 5)
