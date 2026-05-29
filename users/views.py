from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordChangeView as BasePasswordChangeView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login

from .models import User
from .forms import RegisterForm, EditProfileForm

from projects.models import Project


PAGINATE_BY = 12


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return User.objects.all().order_by('-created_at')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(owner=self.get_object())
        return context


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('projects:project_list')


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('projects:project_list')


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('projects:project_list')


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('projects:project_list')

    def get_object(self):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, BasePasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('projects:project_list')
