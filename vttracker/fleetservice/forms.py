from django import forms
from django.utils import timezone
from datetime import date
from fleetservice.models import (
    Binnacle,
    Refuel,
    Service,)

class BinnacleForm(forms.ModelForm):

    class Meta:
        model = Binnacle
        fields = (
            'route',
            'start_kilometer',
            'end_kilometer',
            'start_time',
            'end_time',
        )

        labels = {
            'route': 'Ruta:',
            'start_kilometer': 'Km Inicial:',
            'end_kilometer': 'Km Final:',
            'start_time': 'Hora de Inicio (HH:MM):',
            'end_time': 'Hora de Fin (HH:MM):',
            'fuel_voucher': 'Voucher de Combustible',
        }

        widgets = {
            'route': forms.Select(attrs={'class': 'validate form-control'}),
            'start_kilometer': forms.TextInput(attrs={'class': 'validate form-control'}),
            'end_kilometer': forms.TextInput(attrs={'class': 'validate form-control'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'id': 'timeS', 'class':'validate form-control'}),
            'end_time': forms.TimeInput(attrs={'id': 'timeE', 'class':'validate form-control'}),
            'fuel_voucher': forms.TextInput(attrs={'class': 'validate form-control'}),
        }

    def save(self, commit=True):
        binnacle = super(BinnacleForm, self).save(commit=False)

        binnacle.route = self.cleaned_data['route']
        binnacle.start_kilometer = self.cleaned_data['start_kilometer']
        binnacle.end_kilometer = self.cleaned_data['end_kilometer']
        binnacle.start_time = self.cleaned_data['start_time']
        binnacle.end_time = self.cleaned_data['end_time']
        binnacle.created_at = timezone.now()

        if commit:
            binnacle.save()

        return binnacle

class RefuelForm(forms.ModelForm):

    class Meta:
        model = Refuel
        fields = (
            'liters',
            'amount',
            'datetime',
            'image',
        )

        labels = {
            'liters': 'Litros:',
            'amount': 'Importe:',
            'datetime': 'Fecha: (dd/mm/yyyy)',
            'image': 'Archivo Adjunto:',
        }

        widgets = {
            'liters': forms.TextInput(attrs={'class': 'validate form-control'}),
            'amount': forms.TextInput(attrs={'class': 'validate form-control'}),
            'datetime': forms.DateInput(format='%d/%m/%Y', attrs={'id': 'datepickerA', 'class':'validate form-control'}),
            'image': forms.FileInput(attrs={'class': 'validate form-control'}),
        }

    def save(self, commit=True):
        refuel = super(RefuelForm, self).save(commit=False)

        refuel.liters = self.cleaned_data['liters']
        refuel.amount = self.cleaned_data['amount']
        refuel.datetime = self.cleaned_data['datetime']
        refuel.image = self.cleaned_data['image']

        if commit:
            refuel.save()

        return refuel

class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = (
            'subject',
            'from_depto',
            'start_kilometer',
            'end_kilometer',
            'datetime',
            'start_time',
            'end_time',
            'description',
        )

        labels = {
            'subject': 'Asunto:',
            'from_depto': 'Departamento:',
            'start_kilometer': 'Km Inicial:',
            'end_kilometer': 'Km Final:',
            'datetime': 'Fecha (dd/mm/yyyy):',
            'start_time': 'Hora de Inicio (HH:MM):',
            'end_time': 'Hora de Fin (HH:MM):',
            'description': 'Descripción',
        }

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'validate form-control'}),
            'from_depto': forms.TextInput(attrs={'class': 'validate form-control'}),
            'start_kilometer': forms.TextInput(attrs={'class': 'validate form-control'}),
            'end_kilometer': forms.TextInput(attrs={'class': 'validate form-control'}),
            'datetime': forms.DateInput(format='%d/%m/%Y', attrs={'id': 'datepickerS', 'class':'validate form-control'}),
            'start_time': forms.TimeInput(attrs={'id': 'timeS', 'class':'validate form-control'}),
            'end_time': forms.TimeInput(attrs={'id': 'timeE', 'class':'validate form-control'}),
            'description': forms.Textarea(attrs={'style': 'resize:none', 'class':'validate form-control'}),
        }

    def save(self, commit=True):
        service = super(ServiceForm, self).save(commit=False)

        service.liters = self.cleaned_data['subject']
        service.amount = self.cleaned_data['from_depto']
        service.datetime = self.cleaned_data['start_kilometer']
        service.image = self.cleaned_data['end_kilometer']
        service.datetime = self.cleaned_data['datetime']
        service.start_time = self.cleaned_data['start_time']
        service.end_time = self.cleaned_data['end_time']
        service.image = self.cleaned_data['description']

        if commit:
            service.save()

        return service
