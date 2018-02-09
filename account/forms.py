from django import forms
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        if commit:
            user.save()
        return user
