from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey

class Device(models.Model):
    serial_number = models.CharField(max_length=256, unique=True, primary_key=True)
    name = models.CharField(max_length=100, unique=False)

    class Meta:
        db_table = "device"

    def __str__(self):
        return self.name



class User(models.Model):
    id = models.CharField(max_length=256, unique=True, primary_key=True)
    name = models.CharField(max_length=100, unique=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.name



class GlucoseLevel(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    device = ForeignKey(Device, models.DO_NOTHING)
    user = ForeignKey(User, models.DO_NOTHING)
    recording_type = IntegerField()

    class Meta:
        db_table = "glucose_level"

    def __str__(self):
        return str(self.id) + "--> " + str(self.value) + " - " + str(self.timestamp)
