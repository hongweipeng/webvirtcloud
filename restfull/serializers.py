from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from computes import models as computes_models
from create import models as create_models




class ComputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = computes_models.Compute
        exclude = ('password', )
        
        
class VMTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = create_models.VMTemplate
        exclude = ()

