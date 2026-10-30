from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin/Warden'),
        ('technician', 'Technician'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    # Make roll_no optional in the form (validation will happen in JS/views)
    roll_no = forms.CharField(max_length=50, required=False, help_text="")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'role', 'roll_no')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        roll_no = cleaned_data.get('roll_no')

        # If they selected Student, require the Roll No
        if role == 'student' and not roll_no:
            self.add_error('roll_no', 'Roll number is required for students.')

        # If they are not a student, clear the roll_no to keep DB clean
        if role != 'student':
            cleaned_data['roll_no'] = ''

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.role = self.cleaned_data['role']
        user.roll_no = self.cleaned_data.get('roll_no', '')

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'roll_no')