from django import forms
from .models import Plan, Membresia


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'duracion_dias',
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Plan mensual'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe los beneficios del plan'
            }),

            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            }),

            'duracion_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),

            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
class MembresiaForm(forms.ModelForm):

    class Meta:
        model = Membresia

        fields = [
            'cliente',
            'plan',
            'fecha_inicio',
            'fecha_termino',
            'estado',
        ]

        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),

            'plan': forms.Select(attrs={
                'class': 'form-control'
            }),

            'fecha_inicio': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),

            'fecha_termino': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),

            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['plan'].queryset = Plan.objects.filter(
            activo=True
        ).order_by('nombre')

        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_termino'].input_formats = ['%Y-%m-%d']
