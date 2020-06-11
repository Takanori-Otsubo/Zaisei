from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import (LoginForm, CreateForm, UserUpdateForm, MyPasswordChangeForm,
                    MySetPasswordForm, MyPasswordResetForm)
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from .models import User, Department
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

PASSWORD = "zaiseishibu"


class AuthView(View):
    params = {
        "login_form": LoginForm(),
        "create_form": CreateForm(),
        "login_style": "display: none",
        "create_style": "display: none",
        "create_msg": "",
        "department_list": Department.objects.all()
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("mysite:top"))
        else:
            return render(request, "register/auth.html", AuthView.params)

    def post(self, request, *args, **kwargs):
        if "login" in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect(reverse_lazy("mysite:top"))
            else:
                AuthView.params["login_form"] = login_form
                AuthView.params["login_style"] = "display: block"
                return render(request, "register/auth.html", AuthView.params)

        elif "create" in request.POST:
            create_form = CreateForm(data=request.POST)
            if request.POST["initial_password"] != PASSWORD:
                AuthView.params["create_form"] = create_form
                AuthView.params["create_style"] = "display: block"
                AuthView.params["create_msg"] = "初期パスワードが違います"
                return render(request, "register/auth.html", AuthView.params)
            else:
                if create_form.is_valid():
                    user = create_form.save()
                    login(request, user)
                    return redirect('mysite:top')
                else:
                    AuthView.params["create_form"] = create_form
                    AuthView.params["create_style"] = "display: block"
                    return render(request, "register/auth.html", AuthView.params)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_update.html'
    success_url = reverse_lazy('mysite:top')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_list'] = Department.objects.all()
        return context


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'register/password_change_done.html'


class PasswordForget(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail/register/password_reset/subject.txt'
    email_template_name = 'mail/register/password_reset//message.txt'
    template_name = 'register/password_forget_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_forget_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_forget_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'
