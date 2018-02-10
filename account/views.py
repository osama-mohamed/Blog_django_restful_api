from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('accounts:login')
