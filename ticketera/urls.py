from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('indexApp/', include('app.urls')),
    path('nuevo/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket_edit'),
    path('requerimientos/', views.RequerimientoListView.as_view(), name='ticket_reque'),
    path('requerimientos/<int:pk>/editar/', views.RequerimientoUpdateView.as_view(), name='requerimiento_edit'),
    path('login/', views.login),
    path('logout/', views.logout, name='logout'),
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
    path('mis-tickets/', views.WorkerTicketListView.as_view(template_name='trabajador/worker_ticket_list.html'), name='worker_ticket_list'),
    path('tickets/actualizar_estado/<int:ticket_id>/', views.actualizar_estado_ticket, name='actualizar_estado_ticket'),


]

if settings.DEBUG:  # Solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

