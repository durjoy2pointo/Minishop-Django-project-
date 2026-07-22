from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Address

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )




#================
# address form
#=-===============

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = [
            'address_type',
            'contact_number',
            'division',
            'district',
            'thana',
            'corporation_or_union',
            'area_or_village',
            'additional_info',
        ]

        widgets = {
            'address_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number'
            }),

            'division': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter division'
            }),

            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),

            'thana': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter thana'
            }),

            'corporation_or_union': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter corporation or union'
            }),

            'area_or_village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter area or village'
            }),

            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional address information',
                'rows': 3
            }),
        }

