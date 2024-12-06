from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TicketForm, TicketEditForm, LoginForm
from .models import Ticket, Usuario
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from . import models
from django.core.mail import send_mail
from django.conf import settings
from dirtyfields import DirtyFieldsMixin 
from django.core.paginator import Paginator



def enviar_correo_dinamico(asunto, mensaje, destinatario):
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[destinatario],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False







def enviar_correo(request):
    subject = 'Asunto del correo'
    message = 'Este es el contenido del correo.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['byronignaciocerda@gmail.com']  # Lista de destinatarios

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Correo enviado exitosamente.")
    except Exception as e:
        return HttpResponse(f"Error al enviar el correo: {e}")

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
    request.session.flush()  # Elimina todosa los datos de la sesión actual
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('/login/') 

def ticket_reportes(request):
    return render(request,'ticketReportes')


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
            ticket = form.save()  # Se guarda el ticket en la base de datos

            # Obtener el correo del usuario asignado al ticket
            usuario_asignado = ticket.usuario
            if usuario_asignado and usuario_asignado.email:  # Verifica que el usuario tenga un correo
                asunto = f"Nuevo Ticket Asignado: {ticket.id}"
                mensaje = f"""
                Hola {usuario_asignado.usuar_c_nombre},

                Se te ha asignado un nuevo ticket con los siguientes detalles:
                - ID: {ticket.id}
                - Estado: {ticket.estado.estado_c_nombre if ticket.estado else 'Sin estado'}
                - Prioridad: {ticket.prioridad.prio_c_nombre if ticket.prioridad else 'No definida'}
                - Cliente: {ticket.cliente.clien_c_nombre if ticket.cliente else 'Sin cliente asociado'}

                Por favor, revisa el sistema para más detalles.

                Gracias,
                El equipo de soporte
                """
                enviar_correo_dinamico(asunto, mensaje, usuario_asignado.email)

            return redirect('ticket_list')  # Cambia 'ticket_list' según el nombre de tu vista de listado

        return render(request, 'gestor/ticket_form.html', {'form': form})






class TicketListView(View):
    def get(self, request):
        if 'usuario_id' not in request.session:
            return redirect('/login/')
        
        # Obtenemos todos los tickets
        tickets = Ticket.objects.all()

        # Configuramos la paginación: 10 tickets por página
        paginator = Paginator(tickets, 10)  
        page_number = request.GET.get('page')  # Obtenemos el número de la página actual desde la URL
        page_obj = paginator.get_page(page_number)  # Obtenemos los tickets de la página actual

        # Pasamos la página actual (page_obj) al contexto de la plantilla
        return render(request, 'gestor/ticket_list.html', {'page_obj': page_obj})
    
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
    template_name = 'gestor/ticket_edit.html'  # Reusamos el formulario de creación
    success_url = reverse_lazy('ticket_list')   # Redirige a la lista de tickets tras guardar
