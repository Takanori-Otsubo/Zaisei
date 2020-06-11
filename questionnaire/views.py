from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages
from .output import model_out_put


class QuestionnaireView(LoginRequiredMixin, CreateView):
    template_name = 'questionnaire/coronavirus.html'
    model = CoronaVirusQuestion
    form_class = CoronaVirusForm
    success_url = reverse_lazy('mysite:top')
    success_message = 'アンケートのご回答ありがとうございました。'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.non_error = True

    def form_valid(self, form):
        if self.model.objects.filter(user=self.request.user).exists():
            m = self.model.objects.get(user=self.request.user)
            form = self.form_class(self.request.POST, instance=m)
        form.instance.user = self.request.user
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.model.objects.filter(user=self.request.user).exists():
            context['read'] = '<div id="read"> このアンケートは過去に回答済みなので、回答は上書きします。</div>'
            if self.non_error:
                m = self.model.objects.get(user=self.request.user)
                context['form'] = self.form_class(instance=m)
        else:
            context['read'] = ''
        return context

    def form_invalid(self, form):
        self.non_error = False
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        model_out_put(self.model)
        return self.success_message % cleaned_data


class CoronaVirusView(QuestionnaireView):
    template_name = 'questionnaire/coronavirus.html'
    model = CoronaVirusQuestion
    form_class = CoronaVirusForm
    success_url = reverse_lazy('mysite:top')
