from django import forms
from .models import User, IAM
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .managers import UserManager
'''
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
'''






class UserCreationForm(forms.ModelForm):
    """UserCreationForm()
    A form for creating new users with the given information."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    #: Email associated with the user. Users are identified by this email address. [Jflag repet w/ meta?]
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        """The Meta class creates form fields from model fields. 
        In this case the model being used is :class:`~account.models.User`, and the user's :attr:`~account.models.User.email`
        field is being used."""
        model = User
        #fields = ('email', 'first_name', 'last_name')
        #: Fields used.
        fields = ('email',)

    def clean_password2(self):
        """A function to check that the two passwords provided by the user match."""
        # Check that the two password entries match
        #: User's password.
        password1 = self.cleaned_data.get("password1")
        #: Password confirm.
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2
    #return UserManager.create_user(email, clean_password2())
    '''def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user'''
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.clean_password2())
        user.has_migrated_pwd = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """UserChangeForm()
    A form for changing a user's password."""
    
    #: User's new password
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        """The Meta class creates form fields from model fields. 
        In this case the model being used is :class:`~account.models.User`, and the user's :attr:`~account.models.User.email` and :attr:`~account.models.User.password` 
        fields are being used. [Jflag pass field is inherited for abstract class and not in docs]"""
        model = User
        #: Fields used.
        fields = ('password',)
    def clean_password2(self):
        """A function to check that the two passwords provided by the user match."""
        # Check that the two password entries match
        #: User's password.
        password1 = self.cleaned_data.get("password1")
        #: Password confirm.
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2
    def clean_password(self):
        return self.initial["password"]


class UserLoginForm(forms.ModelForm):
    """UserLoginForm()
    A form for user login using aws credentials."""

    class Meta:
        """The Meta class creates form fields from model fields. 
        In this case the model being used is :class:`~account.models.IAM`, and the user's 
        :attr:`~account.models.IAM.aws_access_key` and :attr:`~account.models.IAM.aws_secret_access_key`
        fields are being used."""
        model = User
        #: Fields used.
        fields = ('email', 'password',)
    #: AWS access key. [Jflag repet w/ meta?]
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'email',
            'type': 'text'
        }
    ))
    #: AWS secret access key. [Jflag repet w/ meta?]
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password',
        }
    ))


class ProfileChangeForm(forms.ModelForm):
    """ProfileChangeForm()
    A form for changing a user's name."""

    class Meta:
        """The Meta class creates form fields from model fields. 
        In this case the model being used is :class:`~account.models.User`, and the user's 
        :attr:`~account.models.User.first_name` and :attr:`~account.models.User.last_name` fields are being used."""
        model = User
        #: Fields used.
        fields = ('first_name', 'last_name',)
