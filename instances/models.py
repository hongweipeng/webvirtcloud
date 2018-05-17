from django.db import models
from computes.models import Compute


class Instance(models.Model):
    compute = models.ForeignKey(Compute, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20)
    uuid = models.CharField(max_length=36)
    is_template = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
