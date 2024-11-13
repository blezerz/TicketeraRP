from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Cliente(models.Model):
    clien_p_id = models.AutoField(primary_key=True)
    clien_c_nombre = models.CharField(max_length=50)
    clien_b_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.clien_c_nombre

# Modelo para tb_departamento
class Departamento(models.Model):
    depto_p_id = models.AutoField(primary_key=True)
    depto_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.depto_c_nombre

# Modelo para tb_descripcion
class Descripcion(models.Model):
    desc_p_id = models.AutoField(primary_key=True)
    desc_c_nombre = models.TextField()

    def __str__(self):
        return self.desc_c_nombre

# Modelo para tb_equipo
class Equipo(models.Model):
    equip_p_id = models.AutoField(primary_key=True)
    equip_c_nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.equip_c_nombre

# Modelo para tb_estado
class Estado(models.Model):
    estado_p_id = models.AutoField(primary_key=True)
    estado_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.estado_c_nombre

# Modelo para tb_perfil
class Perfil(models.Model):
    perf_p_id = models.AutoField(primary_key=True)
    perf_c_nombre = models.CharField(max_length=50)
    perf_b_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.perf_c_nombre

# Modelo para tb_prioridad
class Prioridad(models.Model):
    prio_p_id = models.AutoField(primary_key=True)
    prio_c_nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.prio_c_nombre

# Modelo para tb_tiempo
class Tiempo(models.Model):
    tmpo_p_id = models.AutoField(primary_key=True)
    tmpo_d_hora_inicio = models.DateTimeField(null=True, blank=True)
    tmpo_d_hora_fin = models.DateTimeField(null=True, blank=True)
    tmpo_n_duracion = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.tmpo_d_hora_inicio} - {self.tmpo_d_hora_fin}"

# Modelo para tb_tipo_ticket
class TipoTicket(models.Model):
    tip_p_id = models.AutoField(primary_key=True)
    tip_c_nombre = models.CharField(max_length=50)
    tip_c_detalle = models.CharField(max_length=50)

    def __str__(self):
        return self.tip_c_nombre

# Modelo para tb_requerimiento
class Requerimiento(models.Model):
    reque_p_id = models.AutoField(primary_key=True)
    reque_c_detalle = models.CharField(max_length=50)
    reque_c_observacion = models.CharField(max_length=50)
    clien_p_id = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    tmpo_p_id = models.ForeignKey(Tiempo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.reque_c_detalle

# Modelo para tb_usuario
class Usuario(models.Model):
    usuar_p_id = models.AutoField(primary_key=True)
    perf_p_id = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    equip_p_id = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, blank=True)
    depto_p_id = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    usuar_c_nombre = models.CharField(max_length=100)
    usuar_b_estado = models.BooleanField(default=True)
    usuar_n_rut = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.usuar_c_nombre

# Modelo para tb_ticket
class Ticket(models.Model):
    ticket_p_id = models.AutoField(primary_key=True)
    usuar_p_id = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado_p_id = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    prio_p_id = models.ForeignKey(Prioridad, on_delete=models.SET_NULL, null=True, blank=True)
    desc_p_id = models.ForeignKey(Descripcion, on_delete=models.SET_NULL, null=True, blank=True)
    tmpo_p_id = models.ForeignKey(Tiempo, on_delete=models.SET_NULL, null=True, blank=True)
    reque_p_id = models.ForeignKey(Requerimiento, on_delete=models.SET_NULL, null=True, blank=True)
    tip_p_id = models.ForeignKey(TipoTicket, on_delete=models.SET_NULL, null=True, blank=True)
    clien_p_id = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_p_id}"