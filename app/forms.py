from django import forms
from .models import Ticket, Descripcion, Tiempo, Requerimiento,Usuario

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'usuario', 
            'estado', 
            'prioridad', 
            'descripcion', 
            'tiempo', 
            'requerimiento', 
            'tipo_ticket', 
            'cliente'
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),  # Dropdown para usuarios existentes
            'estado': forms.Select(attrs={'class': 'form-control'}),   # Dropdown para estados
            'prioridad': forms.Select(attrs={'class': 'form-control'}),  # Dropdown para prioridades
            'tipo_ticket': forms.Select(attrs={'class': 'form-control'}),  # Dropdown para tipos de tickets
            'cliente': forms.Select(attrs={'class': 'form-control'}),  # Dropdown para clientes
        }

    # Campos personalizados para crear registros nuevos (I)
    descripcion_nombre = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    tiempo_hora_inicio = forms.DateTimeField(
        label="Hora de Inicio",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    tiempo_hora_fin = forms.DateTimeField(
        label="Hora de Fin",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    tiempo_duracion = forms.IntegerField(
        label="Duración (minutos)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    requerimiento_detalle = forms.CharField(
        label="Detalle del Requerimiento",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    requerimiento_observacion = forms.CharField(
        label="Observación del Requerimiento",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    # Sobrescribimos el método save() para insertar datos en las tablas relacionadas
    def save(self, commit=True):
        # Primero guardamos los datos en las tablas relacionadas
        descripcion = Descripcion.objects.create(desc_c_nombre=self.cleaned_data['descripcion_nombre'])
        tiempo = Tiempo.objects.create(
            tmpo_d_hora_inicio=self.cleaned_data['tiempo_hora_inicio'],
            tmpo_d_hora_fin=self.cleaned_data['tiempo_hora_fin'],
            tmpo_n_duracion=self.cleaned_data['tiempo_duracion']
        )
        requerimiento = Requerimiento.objects.create(
            reque_c_detalle=self.cleaned_data['requerimiento_detalle'],
            reque_c_observacion=self.cleaned_data['requerimiento_observacion'],
            cliente=self.cleaned_data['cliente']
        )

        # Luego asignamos los IDs de las relaciones al ticket
        self.instance.descripcion = descripcion
        self.instance.tiempo = tiempo
        self.instance.requerimiento = requerimiento

        # Finalmente, guardamos el ticket en la base de datos
        return super().save(commit=commit)


class TicketEditForm(forms.ModelForm):
    # Campo para editar la descripción
    descripcion_texto = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    # Campos para editar el tiempo
    tiempo_inicio = forms.DateTimeField(
        label="Hora de Inicio",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )
    tiempo_fin = forms.DateTimeField(
        label="Hora de Fin",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )
    tiempo_duracion = forms.IntegerField(
        label="Duración (minutos)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

    # Campos para editar el requerimiento
    requerimiento_detalle = forms.CharField(
        label="Detalle del Requerimiento",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
    requerimiento_observacion = forms.CharField(
        label="Observación del Requerimiento",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )

    class Meta:
        model = Ticket
        fields = [
            'usuario', 
            'estado', 
            'prioridad', 
            'tipo_ticket', 
            'cliente', 
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'tipo_ticket': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # Inicializar descripción
            if self.instance.descripcion:
                self.fields['descripcion_texto'].initial = self.instance.descripcion.desc_c_nombre
            # Inicializar tiempo
            if self.instance.tiempo:
                self.fields['tiempo_inicio'].initial = self.instance.tiempo.tmpo_d_hora_inicio
                self.fields['tiempo_fin'].initial = self.instance.tiempo.tmpo_d_hora_fin
                self.fields['tiempo_duracion'].initial = self.instance.tiempo.tmpo_n_duracion
            # Inicializar requerimiento
            if self.instance.requerimiento:
                self.fields['requerimiento_detalle'].initial = self.instance.requerimiento.reque_c_detalle
                self.fields['requerimiento_observacion'].initial = self.instance.requerimiento.reque_c_observacion

    def save(self, commit=True):
        # Guardar primero el objeto Ticket
        ticket = super().save(commit=False)

        # Editar o crear la descripción
        descripcion_texto = self.cleaned_data.get('descripcion_texto', '').strip()
        if ticket.descripcion:
            ticket.descripcion.desc_c_nombre = descripcion_texto
            ticket.descripcion.save()
        else:
            descripcion = Descripcion.objects.create(desc_c_nombre=descripcion_texto)
            ticket.descripcion = descripcion

        # Editar o crear el tiempo
        tiempo_inicio = self.cleaned_data.get('tiempo_inicio')
        tiempo_fin = self.cleaned_data.get('tiempo_fin')
        tiempo_duracion = self.cleaned_data.get('tiempo_duracion')
        if ticket.tiempo:
            ticket.tiempo.tmpo_d_hora_inicio = tiempo_inicio
            ticket.tiempo.tmpo_d_hora_fin = tiempo_fin
            ticket.tiempo.tmpo_n_duracion = tiempo_duracion
            ticket.tiempo.save()
        else:
            tiempo = Tiempo.objects.create(
                tmpo_d_hora_inicio=tiempo_inicio,
                tmpo_d_hora_fin=tiempo_fin,
                tmpo_n_duracion=tiempo_duracion
            )
            ticket.tiempo = tiempo

        # Editar o crear el requerimiento
        requerimiento_detalle = self.cleaned_data.get('requerimiento_detalle', '').strip()
        requerimiento_observacion = self.cleaned_data.get('requerimiento_observacion', '').strip()
        if ticket.requerimiento:
            ticket.requerimiento.reque_c_detalle = requerimiento_detalle
            ticket.requerimiento.reque_c_observacion = requerimiento_observacion
            ticket.requerimiento.save()
        else:
            requerimiento = Requerimiento.objects.create(
                reque_c_detalle=requerimiento_detalle,
                reque_c_observacion=requerimiento_observacion,
                cliente=ticket.cliente
            )
            ticket.requerimiento = requerimiento

        if commit:
            ticket.save()
        return ticket