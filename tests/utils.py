from datetime import datetime
from app.models import Visit


async def create_test_visit(
    clinicianId: int = 1,
    patientId: int = 1,
    timestamp: int = datetime.timestamp(datetime.now()),
) -> Visit():

    test_visit = await Visit.create(
        clinicianId=clinicianId,
        patientId=patientId,
        timestamp=timestamp,
    )

    return test_visit


async def create_few_visits():
    for i in range(3):
        await create_test_visit(clinicianId=i, patientId=i)
        await create_test_visit(clinicianId=i, patientId=i+5)
