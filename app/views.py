from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TicketForm, TicketEditForm, LoginForm, RequerimientoForm, RequerimientoEditForm, TicketFilterForm, RequerimientoFilterForm
from .models import Ticket, Usuario, Requerimiento
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                # Buscar el usuario con el nombre proporcionado
                usuario = Usuario.objects.get(usuar_c_nombre=username)
                
                # Comparar la contraseña proporcionada con la almacenada en la base de datos
                if password == usuario.password:  # Comparación directa
                    # Iniciar sesión
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.usuar_c_nombre
                    messages.success(request, f"Bienvenido, {usuario.usuar_c_nombre}")
                    return redirect('/tickets')  # Redirige a la lista de tickets
                else:
                    # Contraseña incorrecta
                    messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                # Usuario no encontrado
                messages.error(request, "Usuario no encontrado.")
        else:
            # Formulario inválido
            messages.error(request, "Formulario inválido")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})





def logout(request):
    # Cierra la sesión del usuario
    request.session.flush()  # Elimina todos los datos de la sesión actual
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('/login/') 




class TicketCreateView(View):
    
    def get(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        form = TicketForm()
        return render(request, 'gestor/ticket_form.html', {'form': form})

    def post(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos del ticket con el requerimiento seleccionado
            return redirect('ticket_list')
        return render(request, 'gestor/ticket_form.html', {'form': form})

# class TicketCreateReque(View):
    
#     def get(self, request):
#         if 'usuario_id' not in request.session:
#             return redirect('/login/')
#         form = TicketForm()
#         return render(request, 'gestor/ticket_reque.html', {'form': form})

#     def post(self, request):
#         if 'usuario_id' not in request.session:
#             return redirect('/login/')
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             form.save()  # Se encarga de guardar los datos en todas las tablas relacionadas
#             return redirect('ticket_list')  # Cambia 'ticket_list' según el nombre de tu vista de listado
#         return render(request, 'gestor/ticket_reque.html', {'form': form})

class TicketListView(View): 
    def get(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        
        # Crear el formulario de filtros
        form = TicketFilterForm(request.GET or None)
        tickets = Ticket.objects.all()

        # Aplicar filtros si se seleccionan
        if form.is_valid():
            estado = form.cleaned_data.get('estado')
            cliente = form.cleaned_data.get('cliente')
            prioridad = form.cleaned_data.get('prioridad')

            if estado:
                tickets = tickets.filter(estado=estado)
            if cliente:
                tickets = tickets.filter(cliente=cliente)
            if prioridad:
                tickets = tickets.filter(prioridad=prioridad)

        return render(request, 'gestor/ticket_list.html', {
            'tickets': tickets,
            'form': form,
        })
    
class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'gestor/ticket_detail.html'
    context_object_name = 'ticket'

    def get_object(self):
        # Busca el ticket por su ID o lanza un 404 si no existe
        return get_object_or_404(Ticket, id=self.kwargs['pk'])
    
class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketEditForm
    template_name = 'gestor/ticket_edit.html'  
    success_url = reverse_lazy('ticket_list')   # Redirige a la lista de tickets tras guardar


class RequerimientoListView(View):
    def get(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        
        # Formularios
        filtro_form = RequerimientoFilterForm(request.GET or None)
        creacion_form = RequerimientoForm()

        # Requerimientos base
        requerimientos = Requerimiento.objects.select_related('cliente').all()

        # Aplicar filtros si se seleccionan
        if filtro_form.is_valid():
            cliente = filtro_form.cleaned_data.get('cliente')
            detalle = filtro_form.cleaned_data.get('detalle')

            if cliente:
                requerimientos = requerimientos.filter(cliente=cliente)
            if detalle:
                requerimientos = requerimientos.filter(reque_c_detalle__icontains=detalle)

        return render(request, 'gestor/requerimiento_list.html', {
            'requerimientos': requerimientos,
            'filtro_form': filtro_form,
            'creacion_form': creacion_form,
        })

    def post(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')

        creacion_form = RequerimientoForm(request.POST)
        filtro_form = RequerimientoFilterForm(request.GET or None)

        if creacion_form.is_valid():
            cliente = creacion_form.cleaned_data.get('cliente')
            if not cliente:
                messages.error(request, "El campo Cliente es obligatorio.")
            else:
                creacion_form.save()
                messages.success(request, "Requerimiento creado con éxito.")
                return redirect('ticket_reque')

        # Si hay un error, volvemos a cargar los requerimientos y los formularios
        requerimientos = Requerimiento.objects.select_related('cliente').all()
        return render(request, 'gestor/requerimiento_list.html', {
            'requerimientos': requerimientos,
            'filtro_form': filtro_form,
            'creacion_form': creacion_form,
        })



class RequerimientoUpdateView(UpdateView):
        
    model = Requerimiento
    form_class = RequerimientoEditForm
    template_name = 'gestor/requerimiento_edit.html'
    success_url = reverse_lazy('ticket_reque')

    def dispatch(self, request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('/login/')  # Redirige al login si no está autenticado
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Requerimiento actualizado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ocurrió un error al actualizar el requerimiento.")
        return super().form_invalid(form)