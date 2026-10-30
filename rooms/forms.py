from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('block', 'room_no', 'room_type', 'capacity', 'occupied', 'status')

    def clean(self):
        cleaned = super().clean()
        capacity = cleaned.get('capacity')
        occupied = cleaned.get('occupied')
        if capacity is not None and occupied is not None and occupied > capacity:
            raise forms.ValidationError('Occupied cannot exceed capacity.')
        return cleaned