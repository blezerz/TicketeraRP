from django import forms
from django.forms import modelformset_factory
from .models import Ticket, Descripcion, Tiempo, Requerimiento,Usuario, Estado, Prioridad, Cliente

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=100, required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
            }))
    password = forms.CharField(label="Contraseña",  required=True, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
            }))

# forms.py
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
            'cliente',
            'archivo_adjunto'
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'tipo_ticket': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'requerimiento': forms.Select(attrs={'class': 'form-control'}),
        }

    #Campo para adjuntar archivos
    archivo_adjunto = forms.FileField(
        label="Archivo Adjunto",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False  
    )

    descripcion_nombre = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'maxlength': 100,
                'rows': 3,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
            }
        ),
        required=True
    )
    tiempo_hora_inicio = forms.DateTimeField(
        label="Fecha de Inicio",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=True  # Campo obligatorio
    )
    tiempo_hora_fin = forms.DateTimeField(
        label="Fecha de Fin",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=True  # Campo obligatorio
    )
    tiempo_duracion = forms.IntegerField(
        label="Duración (hrs)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',             # No permitir valores negativos
            'max': '999',           # No permitir más de 999
            'maxlength': '3',       # Limitar a 3 dígitos (aunque este no es un atributo estándar de input type="number", puede ser útil para navegadores que lo acepten)
            'oninput': 'this.value = Math.max(0, Math.min(999, this.value));'  # Asegura que los valores sean entre 0 y 999 mientras escriben
        }),
        required=True  # Campo obligatorio
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar el queryset y las opciones del campo "requerimiento"
        self.fields['requerimiento'].queryset = Requerimiento.objects.all()
        self.fields['requerimiento'].label = "Seleccionar Requerimiento"
        self.fields['requerimiento'].widget = forms.Select(attrs={'class': 'form-control'})
        
        # Formatear las opciones como `id.- descripción` y añadir una opción vacía al inicio
        self.fields['requerimiento'].choices = [
            ('', 'Selecciona un requerimiento')  # Opción vacía al inicio
        ] + [
            (req.id, f"{req.id}.- {req.reque_c_detalle}")
            for req in Requerimiento.objects.all()
        ]
        
        # Hacer que el campo sea obligatorio
        self.fields['requerimiento'].required = True

        # Aseguramos que los campos del modelo también sean obligatorios
        self.fields['usuario'].required = True
        self.fields['estado'].required = True
        self.fields['prioridad'].required = True
        self.fields['tipo_ticket'].required = True

    # Validación general para asegurarte de que todo cumple las reglas
    def clean(self):
        cleaned_data = super().clean()
        
        # Validaciones personalizadas adicionales si es necesario
        tiempo_inicio = cleaned_data.get('tiempo_hora_inicio')
        tiempo_fin = cleaned_data.get('tiempo_hora_fin')
        
        if tiempo_inicio and tiempo_fin and tiempo_inicio > tiempo_fin:
            self.add_error('tiempo_hora_fin', "La hora de fin no puede ser anterior a la hora de inicio.")
        
        return cleaned_data

    def save(self, commit=True):
        # Primero guardamos los datos en las tablas relacionadas
        descripcion = Descripcion.objects.create(desc_c_nombre=self.cleaned_data['descripcion_nombre'])
        tiempo = Tiempo.objects.create(
            tmpo_d_hora_inicio=self.cleaned_data['tiempo_hora_inicio'],
            tmpo_d_hora_fin=self.cleaned_data['tiempo_hora_fin'],
            tmpo_n_duracion=self.cleaned_data['tiempo_duracion']
        )

        # Asignar el requerimiento seleccionado (en lugar de crear uno nuevo)
        self.instance.requerimiento = self.cleaned_data['requerimiento']

        # Luego asignamos los IDs de las relaciones al ticket
        self.instance.descripcion = descripcion
        self.instance.tiempo = tiempo

        # Asignar el archivo adjunto al ticket (si se proporciona)
        archivo_adjunto = self.cleaned_data.get('archivo_adjunto')
        if archivo_adjunto:
            self.instance.archivo_adjunto = archivo_adjunto

        # Finalmente, guardamos el ticket en la base de datos
        return super().save(commit=commit)



class TicketEditForm(forms.ModelForm):
    # Campo para editar la descripción
    descripcion_texto = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
                              attrs={
                'class': 'form-control',
                'maxlength': 100,
                'rows': 3,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
            }),
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
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',             # No permitir valores negativos
            'max': '999',           # No permitir más de 999
            'maxlength': '3',       # Limitar a 3 dígitos (aunque este no es un atributo estándar de input type="number", puede ser útil para navegadores que lo acepten)
            'oninput': 'this.value = Math.max(0, Math.min(999, this.value));'  # Asegura que los valores sean entre 0 y 999 mientras escriben
        }),
        required=False
    )

    # Campo para seleccionar un requerimiento existente
    requerimiento = forms.ChoiceField(
        label="Seleccionar Requerimiento",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # Campo obligatorio
    )
    
    archivo_adjunto = forms.FileField(
        label="Archivo Adjunto (opcional)",
        required=False,  # Este campo es opcional
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False})
    )

    class Meta:
        model = Ticket
        fields = [
            'usuario',
            'estado',
            'prioridad',
            'tipo_ticket',
            'cliente',
            'archivo_adjunto',  # Agregar el campo de archivo

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

        # Configurar el dropdown para requerimientos
        self.fields['requerimiento'].choices = [
            ('', 'Selecciona un requerimiento')  # Opción vacía al inicio
        ] + [
            (req.id, f"{req.id}.- {req.reque_c_detalle}")
            for req in Requerimiento.objects.all()
        ]

        # Preseleccionar el requerimiento actual del ticket, si existe
        if self.instance.requerimiento:
            self.fields['requerimiento'].initial = self.instance.requerimiento.id

    def save(self, commit=True):
        # Guardar primero el objeto Ticket
        ticket = super().save(commit=False)

        # Editar o asignar el requerimiento seleccionado
        requerimiento_id = self.cleaned_data.get('requerimiento')
        if requerimiento_id:
            ticket.requerimiento = Requerimiento.objects.get(id=requerimiento_id)

        # Guardar otros campos relacionados
        descripcion_texto = self.cleaned_data.get('descripcion_texto', '').strip()
        if ticket.descripcion:
            ticket.descripcion.desc_c_nombre = descripcion_texto
            ticket.descripcion.save()
        else:
            descripcion = Descripcion.objects.create(desc_c_nombre=descripcion_texto)
            ticket.descripcion = descripcion

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

        if commit:
            ticket.save()
        return ticket
    

class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['cliente', 'reque_c_detalle', 'reque_c_observacion']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'reque_c_detalle': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': 100,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
                'placeholder': 'Ingrese el detalle del requerimiento',
            }),
            'reque_c_observacion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
                'placeholder': 'Ingrese una observación',
            }),
        }
        labels = {
            'cliente': 'Cliente',
            'reque_c_detalle': 'Detalle del Requerimiento',
            'reque_c_observacion': 'Observación ',
        }
    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError("El campo Cliente es obligatorio.")
        return cliente
    
class RequerimientoEditForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['cliente', 'reque_c_detalle', 'reque_c_observacion']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'reque_c_detalle': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'rows': 2,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
                'placeholder': 'Ingrese el detalle del requerimiento',
            }),
            'reque_c_observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'rows': 2,
                'oninput': "validarCaracteresProhibidos(this)",  # Llama a la función JavaScript
                'placeholder': 'Ingrese una observación',
            }),
        }
        labels = {
            'cliente': 'Cliente',
            'reque_c_detalle': 'Detalle del Requerimiento',
            'reque_c_observacion': 'Observación',
        }

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError("El campo Cliente es obligatorio.")
        return cliente

# Filtros para Lista de Ticket y Requerimiento
class TicketFilterForm(forms.Form):
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label="Cliente",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prioridad = forms.ModelChoiceField(
        queryset=Prioridad.objects.all(),
        label="Prioridad",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class RequerimientoFilterForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label="Cliente",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    detalle = forms.CharField(
        label="Detalle",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )