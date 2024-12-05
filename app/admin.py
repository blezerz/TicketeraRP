from django.contrib import admin
from app.models import Cliente, Departamento, Descripcion, Equipo,Perfil,Prioridad, Tiempo, TipoTicket,Requerimiento, Usuario,Ticket,Estado


# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display =["id","clien_c_nombre","clien_b_activo"]
admin.site.register(Cliente,ClienteAdmin)


class DepartamentoAdmin(admin.ModelAdmin):
    list_display =["id","depto_c_nombre"]
admin.site.register(Departamento,DepartamentoAdmin)

class DescripcionAdmin(admin.ModelAdmin):
    list_display =["id","desc_c_nombre"]
admin.site.register(Descripcion,DescripcionAdmin)

class EquipoAdmin(admin.ModelAdmin):
    list_display=["id","equip_c_nombre"]
admin.site.register(Equipo,EquipoAdmin)


class EstadoAdmin(admin.ModelAdmin):
    list_display=["id","estado_c_nombre"]
admin.site.register(Estado,EstadoAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display=["id","perf_c_nombre","perf_b_activo"]
admin.site.register(Perfil,PerfilAdmin)


class PrioridadAdmin(admin.ModelAdmin):
    list_display=["id","prio_c_nombre"]
admin.site.register(Prioridad,PrioridadAdmin)


class TiempoAdmin(admin.ModelAdmin):
    list_display=["id","tmpo_d_hora_inicio","tmpo_d_hora_fin","tmpo_n_duracion"]
admin.site.register(Tiempo,TiempoAdmin)

class TipoTicketAdmin(admin.ModelAdmin):
    list_display=["id","tip_c_nombre","tip_c_detalle"]
admin.site.register(TipoTicket,TipoTicketAdmin)

class RequerimientoAdmin(admin.ModelAdmin):
    list_display=["id","reque_c_detalle","reque_c_observacion","cliente","tiempo"]
admin.site.register(Requerimiento,RequerimientoAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display=["id","perfil","equipo","departamento","usuar_c_nombre","usuar_b_estado","usuar_n_rut"]
admin.site.register(Usuario,UsuarioAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display=["id","usuario","estado","prioridad","descripcion","tiempo","requerimiento","tipo_ticket","cliente"]
admin.site.register(Ticket,TicketAdmin)

#from django.contrib import admin
#from mainApp.models import Producto
# Register your models here.

#class ProductoAdmin(admin.ModelAdmin):
#    lista_display =["id","nombre","precio","stock","reorden"]
#admin.site.register(Producto,ProductoAdmin)

