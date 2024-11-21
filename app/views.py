from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TicketForm, TicketEditForm
from .models import Ticket
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy


class TicketCreateView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'gestor/ticket_form.html', {'form': form})

    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()  # Se encarga de guardar los datos en todas las tablas relacionadas
            return redirect('ticket_list')  # Cambia 'ticket_list' según el nombre de tu vista de listado
        return render(request, 'gestor/ticket_form.html', {'form': form})


class TicketListView(View):
    def get(self, request):
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
    template_name = 'gestor/ticket_edit.html'  # Reusamos el formulario de creación
    success_url = reverse_lazy('ticket_list')   # Redirige a la lista de tickets tras guardar
