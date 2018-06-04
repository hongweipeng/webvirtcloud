from rest_framework import serializers
from computes import models as computes_models
from django.core.exceptions import ObjectDoesNotExist



class ComputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = computes_models.Compute
        exclude = ('password', )