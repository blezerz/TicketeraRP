from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TicketForm, TicketEditForm, LoginForm, RequerimientoForm, RequerimientoEditForm
from .models import Ticket, Usuario, Requerimiento
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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
        # Obtenemos todos los tickets de la base de datos
        tickets = Ticket.objects.all()
        return render(request, 'gestor/ticket_list.html', {'tickets': tickets})
    
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
        
        requerimientos = Requerimiento.objects.select_related('cliente').all()
        form = RequerimientoForm()
        return render(request, 'gestor/requerimiento_list.html', {
            'requerimientos': requerimientos,
            'form': form
        })

    def post(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        
        form = RequerimientoForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data.get('cliente')
            if not cliente:
                messages.error(request, "El campo Cliente es obligatorio.")
            else:
                form.save()
                messages.success(request, "Requerimiento creado con éxito.")
                return redirect('ticket_reque')
        
        requerimientos = Requerimiento.objects.select_related('cliente').all()
        return render(request, 'gestor/requerimiento_list.html', {
            'requerimientos': requerimientos,
            'form': form
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