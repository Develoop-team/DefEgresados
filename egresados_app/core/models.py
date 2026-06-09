from django.db import models
# funcionamiento del sistema:
# 1 el admin carga prendas,
# 2 carga colegios
# 3 "" una promoción,
# 4 "" uno o más cursos,
# 4 "" alumnos
# 5 "" pedido
# 6 "" detalle pedido


class Colegio(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    email = models.CharField(max_length=150)
    contacto_responsable = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return self.nombre


class Presupuesto(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    #colegio = models.ForeignKey(Colegio, on_delete=models.SET_NULL, null=True, blank=True)
    colegio = models.TextField(blank=True, null=True)
    provincia = models.TextField(blank=True, null=True)
    localidad = models.TextField(blank=True, null=True)
    nombre_contacto = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    cantidad_estimada = models.IntegerField(blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    diseno = models.URLField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
    fecha = models.DateField()

    def __str__(self):
        return f"Presupuesto #{self.pk} - {self.nombre_contacto}"

class Promocion(models.Model):
    nombre = models.CharField(max_length=150)
    anio = models.IntegerField()
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)

    fecha_creacion = models.DateField(auto_now_add=True)

    ESTADO_CHOICES = [
        ('armando', 'Armando'),
        ('presupuestada', 'Presupuestada'),
        ('confirmada', 'Confirmada'),
        ('produccion', 'Producción'),
        ('finalizada', 'Finalizada'),
    ]

    estado = models.CharField(
        max_length=30,
        choices=ESTADO_CHOICES,
        default='armando'
    )

    def __str__(self):
        return f"{self.nombre} ({self.anio})"

class Curso(models.Model):
    TURNO_CHOICES = [
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ]
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True, blank=True)
    division = models.CharField(max_length=100)
    anio_egreso = models.IntegerField()
    turno = models.CharField(
        max_length=30,
        choices=TURNO_CHOICES,
        default='mañana')
    cantidad_alumnos = models.IntegerField()

    def __str__(self):
        return f"{self.colegio} | {self.division} ({self.anio_egreso}) - {self.turno}"



class Alumno(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    telefono_tutor = models.CharField(max_length=30, blank=True, null=True)
    nombre_tutor = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Prenda(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_prenda = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    color_base = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Admin(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_produccion', 'En producción'),
        ('entregado', 'Entregado'),
    ]
    promo = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.promo}"

# class Talla(models.Model):
#     TALLA_CHOICES = [
#         ('s', 'S'),
#         ('m', 'M'),
#         ('l', 'L'),
#         ('xl', 'XL'),
#         ('xxl', 'XXL'),
#     ]
#     nombre = models.CharField(max_length=30, choices=TALLA_CHOICES)

#     def __str__(self):
#         return self.nombre

class DetallePedido(models.Model):
    ESTADO_ITEM_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_produccion', 'En producción'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
    ]
    TALLA_CHOICES = [
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT)
    talla = models.CharField(
        max_length=10,
        choices=TALLA_CHOICES,
        default='s')
    personalizacion = models.TextField(blank=True, null=True)
    apodo = models.CharField(max_length=100, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # estado_item = models.CharField(
    #     max_length=30,
    #     choices=ESTADO_ITEM_CHOICES,
    #     default='pendiente')

    def __str__(self):
        return f"Detalle #{self.pk} - {self.alumno} / {self.prenda}"



class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    detalle = models.ForeignKey(DetallePedido, on_delete=models.CASCADE)
    numero_cuota = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
    comprobante_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Pago #{self.pk} - Cuota {self.numero_cuota} - {self.alumno}"


class Recibo(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    numero_recibo = models.CharField(max_length=50)
    fecha_emision = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Recibo {self.numero_recibo}"

