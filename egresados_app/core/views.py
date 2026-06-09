from rest_framework import viewsets
from .models import Colegio
from .serializers import ColegioSerializer
from .models import Colegio, Promocion, Curso, Alumno, Pedido
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Presupuesto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from cloudinary.uploader import upload


@csrf_exempt
@csrf_exempt
def enviar_solicitud(request):

    if request.method == "POST":

        archivo = request.FILES.get("diseno")

        url_archivo = None

        if archivo:
            resultado = upload(
                archivo,
                folder="solicitudes"
            )

            url_archivo = resultado["secure_url"]

        Presupuesto.objects.create(
            provincia=request.POST.get('provincia'),
            localidad=request.POST.get('localidad'),
            colegio=request.POST.get('colegio'),
            nombre_contacto=request.POST.get('nombre_contacto'),
            email=request.POST.get('email'),
            cantidad_estimada=request.POST.get('cantidad_estimada'),
            mensaje=request.POST.get('mensaje'),
            diseno=url_archivo,
            fecha=timezone.now().date()
        )

        return JsonResponse({
            "success": True,
            "message": "Solicitud enviada correctamente"
        })




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

def dashboard(request):
    colegios = Colegio.objects.all()

    return render(request,
                  'admin_panel/dashboard.html',
                  {'colegios': colegios})