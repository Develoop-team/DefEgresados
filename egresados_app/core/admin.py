from django.contrib import admin

# Register your models here.
from .models import (
    Colegio, Presupuesto, Curso, Alumno,
    Prenda, Admin, Pedido, DetallePedido, Pago, Recibo, Promocion
)


@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'email')
    search_fields = ('nombre', 'email')
    list_filter = ()


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_contacto','colegio','provincia','localidad', 'email', 'cantidad_estimada', 'mensaje', 'estado', 'fecha')
    search_fields = ('nombre_contacto',)
    list_filter = ('estado', 'fecha')

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'anio', 'colegio', 'estado', 'fecha_creacion')
    search_fields = ('colegio',)
    list_filter = ()

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'division', 'colegio', 'anio_egreso', 'promocion', 'turno', 'cantidad_alumnos')
    search_fields = ('division',)
    list_filter = ('anio_egreso', 'turno', 'colegio')


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apellido', 'nombre', 'dni', 'curso')
    search_fields = ('apellido', 'nombre', 'dni')
    list_filter = ('curso__colegio',)


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_prenda', 'modelo', 'precio_base', 'activo')
    search_fields = ('nombre', 'tipo_prenda')
    list_filter = ('activo', 'tipo_prenda')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'rol', 'activo')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'activo')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'promo', 'admin', 'fecha', 'estado')
    search_fields = ('promo',)
    list_filter = ('estado', 'fecha', 'promo')


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    # list_display = ('id', 'pedido', 'alumno', 'prenda', 'apodo','talla', 'precio_unitario', 'estado_item')
    list_display = ('id', 'pedido', 'alumno', 'prenda', 'apodo','talla', 'precio_unitario')
    search_fields = ('alumno__apellido', 'prenda__nombre')
    # list_filter = ('estado_item', 'talla', 'prenda')
    list_filter = ('talla', 'prenda')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'numero_cuota', 'monto', 'fecha_vencimiento', 'fecha_pago', 'estado')
    search_fields = ('alumno__apellido', 'alumno__nombre')
    list_filter = ('estado', 'fecha_vencimiento')


@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_recibo', 'pago', 'fecha_emision', 'monto')
    search_fields = ('numero_recibo',)
    list_filter = ('fecha_emision',)



