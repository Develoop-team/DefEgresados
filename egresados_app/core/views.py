from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Presupuesto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def enviar_solicitud(request):
    if request.method == 'POST':

        Presupuesto.objects.create(
            provincia=request.POST.get('provincia'),
            localidad=request.POST.get('localidad'),
            nombre_contacto=request.POST.get('nombre_contacto'),
            telefono=request.POST.get('telefono'),
            cantidad_estimada=request.POST.get('cantidad_estimada'),
            mensaje=request.POST.get('mensaje'),
            fecha=timezone.now().date()
        )

        # return redirect('home')
        return JsonResponse({
            "success": True,
            "message": "Solicitud enviada correctamente"
})

# Create your views here.
