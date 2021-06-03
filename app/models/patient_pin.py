from tortoise import fields
from tortoise.models import Model


class PatientPin(Model):
    class Meta:
        table = "patientPins"

    id = fields.IntField(pk=True)
    clinicianId = fields.IntField()
    patientId = fields.IntField()
    timestamp = fields.IntField()
