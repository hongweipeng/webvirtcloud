from django.db import models
from computes.models import Compute
from django.utils import timezone


class Instance(models.Model):
    compute = models.ForeignKey(Compute, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    uuid = models.CharField(max_length=36)
    is_template = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
