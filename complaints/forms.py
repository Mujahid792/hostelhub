from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('category', 'title', 'description', 'image', 'priority')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AssignForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('assigned_to', 'status')