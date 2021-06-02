from tortoise import fields
from tortoise.models import Model


class Visit(Model):
    id = fields.IntField(pk=True)
    clinicianId = fields.IntField()
    patientId = fields.IntField()
    timestamp = fields.IntField()
