from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class Login(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/login.html'

    # 로그인 아이디와 패스워드가 적합한지 체크 후 로그인 처리
    def form_valid(self, form):
        username = form.cleaned_data.get("username")  # 전달받은 username의 데이터가 clean한지
        password = form.cleaned_data.get("password")  # 전달받은 password의 데이터가 clean한지
        user = authenticate(self.request, username=username, password=password)  # username과 password가 DB에 있는지 없으면 None반환
        if user is not None:
            # user가 none이 아니면 로그인 처리 해주라
            login(
                self.request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
        return super().form_valid(form)


# def logout(request):
#     logout(request)
#     return redirect(reverse("login"))

class Logout(LogoutView):
    next_page = 'index'
