
from computes import models as computes_models
from . import serializers
from rest_framework.views import APIView
from rest_framework import mixins, generics


class ComputerList(generics.ListAPIView):
    queryset = computes_models.Compute.objects.all()
    serializer_class = serializers.ComputeSerializer

























