from django.db import models

# Create your models here.
class Cliente(models.Model):
    clien_c_nombre = models.CharField(max_length=50)
    clien_b_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.clien_c_nombre

# Modelo para tb_departamento
class Departamento(models.Model):
    depto_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.depto_c_nombre

# Modelo para tb_descripcion
class Descripcion(models.Model):
    desc_c_nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.desc_c_nombre

# Modelo para tb_equipo
class Equipo(models.Model):
    equip_c_nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.equip_c_nombre

# Modelo para tb_estado
class Estado(models.Model):
    estado_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.estado_c_nombre

# Modelo para tb_perfil
class Perfil(models.Model):
    perf_c_nombre = models.CharField(max_length=50)
    perf_b_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.perf_c_nombre

# Modelo para tb_prioridad
class Prioridad(models.Model):
    prio_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.prio_c_nombre

# Modelo para tb_tiempo
class Tiempo(models.Model):
    tmpo_d_hora_inicio = models.DateTimeField(null=True, blank=True)
    tmpo_d_hora_fin = models.DateTimeField(null=True, blank=True)
    tmpo_n_duracion = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.tmpo_d_hora_inicio} - {self.tmpo_d_hora_fin}"
    
     # Método para formatear las fechas
    def formato_fecha_inicio(self):
        return self.tmpo_d_hora_inicio.strftime('%d/%m/%Y') if self.tmpo_d_hora_inicio else 'N/A'

    def formato_fecha_fin(self):
        return self.tmpo_d_hora_fin.strftime('%d/%m/%Y') if self.tmpo_d_hora_fin else 'N/A'

# Modelo para tb_tipo_ticket
class TipoTicket(models.Model):
    tip_c_nombre = models.CharField(max_length=50)
    tip_c_detalle = models.CharField(max_length=100)

    def __str__(self):
        return self.tip_c_nombre

# Modelo para tb_requerimiento
class Requerimiento(models.Model):
    reque_c_detalle = models.CharField(max_length=100)
    reque_c_observacion = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    tiempo = models.ForeignKey(Tiempo, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.reque_c_detalle

# Modelo para tb_usuario
class Usuario(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    usuar_c_nombre = models.CharField(max_length=100)
    usuar_b_estado = models.BooleanField(default=True)
    usuar_n_rut = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=12, default='secret')
    email = models.EmailField(max_length=255, unique=False)

    def __str__(self):
        return self.usuar_c_nombre
    
    
# Modelo para tb_ticket
class Ticket(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.ForeignKey(Descripcion, on_delete=models.SET_NULL, null=True, blank=True)
    tiempo = models.ForeignKey(Tiempo, on_delete=models.SET_NULL, null=True, blank=True)
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_ticket = models.ForeignKey(TipoTicket, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    archivo_adjunto = models.FileField(upload_to='archivos_adjuntos/', null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id}"
    