from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "user_type")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['user_type'].label = "Хто ви?"
        self.fields['email'].label = "Email"
