from django.db import models
# funcionamiento del sistema:
# 1 el admin carga prendas,
# 2 carga colegios
# 3 "" un curso,
# 4 "" un alumno
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
    colegio = models.ForeignKey(Colegio, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_contacto = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    cantidad_estimada = models.IntegerField(blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
    fecha = models.DateField()

    def __str__(self):
        return f"Presupuesto #{self.pk} - {self.nombre_contacto}"


class Curso(models.Model):
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    nombre_curso = models.CharField(max_length=100)
    anio_egreso = models.IntegerField()
    turno = models.CharField(max_length=30)
    cantidad_alumnos = models.IntegerField()

    def __str__(self):
        return f"{self.colegio} | {self.nombre_curso} ({self.anio_egreso}) - {self.turno}"


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
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.curso}"


class DetallePedido(models.Model):
    ESTADO_ITEM_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_produccion', 'En producción'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT)
    talla = models.CharField(max_length=20, blank=True, null=True)
    personalizacion = models.TextField(blank=True, null=True)
    apodo = models.CharField(max_length=100, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    estado_item = models.CharField(
        max_length=30,
        choices=ESTADO_ITEM_CHOICES,
        default='pendiente')

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