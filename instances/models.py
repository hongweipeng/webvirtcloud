from django.db import models
from computes.models import Compute
from django.utils import timezone


class Instance(models.Model):
# <<<<<<< HEAD
    compute = models.ForeignKey(Compute, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=63)
# =======
    # compute = models.ForeignKey(Compute, on_delete=models.CASCADE)
    # name = models.CharField(max_length=120)
# >>>>>>> 3748a46d8fef7bca5628b5b9021dd1968adfa7ed
    uuid = models.CharField(max_length=36)
    is_template = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
