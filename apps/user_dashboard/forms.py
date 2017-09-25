from django import forms
from models import *
import re
import bcrypt
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
class SignInForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    def clean(self):
        data = self.cleaned_data
        user = User.objects.filter(email=data.get("email"))
        if not user:
            self.add_error("email", "That email is not registered")
        elif not bcrypt.checkpw(data.get("password").encode(), user[0].hashed_pw.encode()):
            self.add_error("password", "Incorrect password")

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput)
    def clean(self):
        data = self.cleaned_data
        if len(data.get("first_name")) < 2:
            self.add_error("first_name", "First name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("first_name")):
            self.add_error("first_name", "First name must have only alphabetic characters")
        if len(data.get("last_name")) < 2:
            self.add_error("last_name", "Last name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("last_name")):
            self.add_error("last_name", "Last name must have only alphabetic characters")
        if data.get("password") != data.get("password_confirmation"):
            self.add_error("password_confirmation", "Password confirmation must match")

class UpdateInfo(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    def clean(self):
        data = self.cleaned_data
        if len(data.get("first_name")) < 2:
            self.add_error("first_name", "First name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("first_name")):
            self.add_error("first_name", "First name must have only alphabetic characters")
        if len(data.get("last_name")) < 2:
            self.add_error("last_name", "Last name must be at least 2 characters")
        if not LETTER_REGEX.match(data.get("last_name")):
            self.add_error("last_name", "Last name must have only alphabetic characters")

class UpdateInfoAdmin(UpdateInfo):
    user_level = forms.ChoiceField(choices=((1, "Normal"), (9, "Admin")))

class ChangePassword(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput)
    def clean(self):
        data = self.cleaned_data
        if data.get("password") != data.get("password_confirmation"):
            self.add_error("password_confirmation", "Password confirmation must match")

class EditDescription(forms.Form):
    description = forms.CharField(max_length=255, widget=forms.Textarea, required=False)

class MessageForm(forms.Form):
    message = forms.CharField(max_length=255, widget=forms.Textarea)

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=255, widget=forms.Textarea)