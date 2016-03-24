from django.db import models

from cmis_storage.storage import CMISStorage


class TestModel(models.Model):
    document = models.FileField(storage=CMISStorage())

    class Meta:
        app_label = 'cmis_storage'
