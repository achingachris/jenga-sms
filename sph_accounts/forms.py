from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    public_email = forms.CharField(widget=forms.EmailInput(attrs={ 'class': 'form-control' }), max_length=254, required=False)
    # url = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    # bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'public_email', 'institution', 'location']

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile