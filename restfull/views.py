from . import serializers
from rest_framework.views import APIView
from rest_framework import mixins, generics

from computes import models as computes_models
from create import models as create_models

class ComputerList(generics.ListAPIView):
    queryset = computes_models.Compute.objects.all()
    serializer_class = serializers.ComputeSerializer

class ComputerDetail(generics.RetrieveAPIView):
    queryset = computes_models.Compute.objects.all()
    serializer_class = serializers.ComputeSerializer


class VMTempList(generics.ListAPIView):
    queryset = create_models.VMTemplate.objects.all()
    serializer_class = serializers.VMTempSerializer





















