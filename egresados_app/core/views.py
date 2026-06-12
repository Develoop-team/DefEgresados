from django.utils import timezone
from rest_framework import viewsets
from .models import Colegio
from .serializers import ColegioSerializer
from .models import Colegio, Promocion, Curso, Alumno, Pedido
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path, include
from .models import Colegio, Pago, Presupuesto

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
    #colegios = Colegio.objects.all()
    solicitudes = Presupuesto.objects.order_by('-fecha')
    return render(request,
                  'admin_panel/dashboard.html',
                  #{'colegios': colegios}
                  {'solicitudes': solicitudes}
                  )



# enviar comprobante de pago tutor
# bucar x dni
def comprobante_cuota(request):
    alumno = None
    pagos = []
    error = None
    comprobante_enviado = False

    if request.method == 'POST':

        # busca x dni
        if 'dni' in request.POST:
            dni = request.POST.get('dni', '').strip()
            try:
                alumno = Alumno.objects.get(dni=dni)
                pagos = Pago.objects.filter(alumno=alumno, estado__in=['pendiente', 'en_revision'])
            except Alumno.DoesNotExist:
                error = "No se encontró ningún alumno con ese DNI."

        #  subir comprobante
        elif 'pago_id' in request.POST:
            pago_id = request.POST.get('pago_id')
            pago = get_object_or_404(Pago, id=pago_id)
            if request.FILES.get('comprobante'):
                pago.comprobante = request.FILES['comprobante']
                pago.estado = 'en_revision'
                pago.fecha_envio_comprobante = timezone.now()
                pago.save()
                comprobante_enviado = True
                alumno = pago.alumno

    return render(request, 'comprobantes/subir_comprobante.html', {
        'alumno': alumno,
        'pagos': pagos,
        'error': error,
        'comprobante_enviado': comprobante_enviado,
    })


#comprobante de pago parte admin

def gestion_comprobantes(request):
    pagos = Pago.objects.filter(estado='en_revision').select_related('alumno', 'detalle')

    if request.method == 'POST':
        pago_id = request.POST.get('pago_id')
        accion = request.POST.get('accion')
        pago = get_object_or_404(Pago, id=pago_id)

        if accion == 'aprobar':
            pago.estado = 'pagado'
            pago.fecha_pago = timezone.now().date()
            pago.save()

        elif accion == 'rechazar':
            pago.estado = 'pendiente'
            pago.comprobante = None
            pago.fecha_envio_comprobante = None
            pago.save()

        return redirect('gestion_comprobantes')

    return render(request, 'admin_panel/gestion_comprobantes.html', {'pagos': pagos})
# fin comprobante de pago