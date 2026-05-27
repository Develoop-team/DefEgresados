from rest_framework import viewsets
from .models import Colegio
from .serializers import ColegioSerializer

class ColegioViewSet(viewsets.ModelViewSet):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer
