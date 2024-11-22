from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('indexApp/', include('app.urls')),
    path('nuevo/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/edit/', views.TicketUpdateView.as_view(), name='ticket_edit'),
    path('login/', views.login),
    path('logout/', views.logout, name='logout')

]
