from rest_framework import viewsets
from .models import Colegio
from .serializers import ColegioSerializer
from .models import Colegio, Promocion, Curso, Alumno, Pedido
from django.shortcuts import render
from django.urls import path, include
from .models import Colegio

class ColegioViewSet(viewsets.ModelViewSet):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer

# HOME
def home(request):
    colegios = Colegio.objects.all()

    colegio_id = request.GET.get('colegio')
    promo_id = request.GET.get('promo')

    colegio_sel = None
    promociones = None
    promo_sel = None
    cursos = None

    if colegio_id:
        colegio_sel = Colegio.objects.get(pk=colegio_id)
        promociones = Promocion.objects.filter(colegio=colegio_sel)

    if promo_id:
        promo_sel = Promocion.objects.get(pk=promo_id)
        cursos = Curso.objects.filter(promocion=promo_sel).prefetch_related('alumno_set')

    return render(request, 'home.html', {
        'colegios': colegios,
        'colegio_sel': colegio_sel,
        'promociones': promociones,
        'promo_sel': promo_sel,
        'cursos': cursos,
    })


# COLEGIOS
def lista_colegios(request):
    colegios = Colegio.objects.all()
    return render(request, 'colegios/lista.html', {'colegios': colegios})