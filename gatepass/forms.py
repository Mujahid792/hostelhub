from django import forms
from .models import GatePass

class GatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = ('reason', 'destination', 'departure_date', 'return_date')
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        dep = cleaned.get('departure_date')
        ret = cleaned.get('return_date')
        if dep and ret and ret < dep:
            raise forms.ValidationError('Return date must be after departure date.')
        return cleaned