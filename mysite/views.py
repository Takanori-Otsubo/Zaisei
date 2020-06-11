from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, YearArchiveView, MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from .models import *
from .mixins import *
from django.http import Http404
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.shortcuts import redirect
import questionnaire.models
import inspect


class TopView(LoginRequiredMixin, TemplateView):
    template_name = 'mysite/top.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.q_flag = False
        self.q_title = ""
        self.q_url = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = int(str(datetime.datetime.today().date()).replace("-", ""))
        classes = list(map(lambda x: x[1], inspect.getmembers(questionnaire.models, inspect.isclass)))
        ms = list(filter(lambda x: hasattr(x, 'deadline'), classes))

        for i in sorted(ms, key=lambda x: x.deadline):
            if today < i.deadline:
                if not i.objects.filter(user=self.request.user).exists():
                    self.model = i
                    self.q_flag = True
                    self.q_title = self.model.title
                    self.q_url = self.model.url
                    break
        context['q_flag'] = self.q_flag
        context['q_title'] = self.q_title
        context['q_url'] = self.q_url
        return context


class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'mysite/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class CircularIndexView(LoginRequiredMixin, ListView):
    model = Circular
    template_name = 'mysite/circular.html'
    paginate_by = 10


class StandardIndexView(LoginRequiredMixin, ListView):
    model = Standard
    template_name = 'mysite/standard.html'


class PostIndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'mysite/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_content_html'] = "mysite/snippets/post_index.html"
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'mysite/index.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        if not self.request.user in obj.user.all():
            obj.user.add(self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_content_html'] = "mysite/snippets/post_detail.html"
        return context


class CategoryIndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'mysite/index.html'
    paginate_by = 5

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['post_content_html'] = "mysite/snippets/category_index.html"
        return context


class PostYearArchive(LoginRequiredMixin, YearArchiveView):
    model = Post
    template_name = 'mysite/index.html'
    date_field = 'published_at'
    paginate_by = 5
    make_object_list = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_content_html'] = "mysite/snippets/year_archive_index.html"
        return context


class PostMonthArchive(LoginRequiredMixin, MonthArchiveView):
    model = Post
    template_name = 'mysite/index.html'
    date_field = 'published_at'
    paginate_by = 5
    make_object_list = True
    month_format = '%m'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_content_html'] = "mysite/snippets/month_archive_index.html"
        return context


def add_event_join(request, pk):
    d = {}
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.user.add(request.user)
        d = {'count': str(event.user.count())}
    return JsonResponse(d)


def remove_event_join(request, pk):
    d = {}
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.user.remove(request.user)
        if event.level > request.user.level:
            level_color = 'executive'
        else:
            level_color = 'possible'
        d = {'count': str(event.user.count()),
             'level_color': level_color}
    return JsonResponse(d)


def add_circular_user(request, pk):
    d = {}
    circular = get_object_or_404(Circular, pk=pk)
    print("start")
    if request.method == 'POST':
        if not request.user in circular.user.all():
            circular.user.add(request.user)
            d = {'flag': True}
            print(f'{request.user} is not in {circular}')
        else:
            print(f'{request.user} is in {circular}')
    return JsonResponse(d)


def add_post_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        text = request.POST["text"]
        displayed_user = request.POST["user-name"]
        user = request.user
        if post.level == 1:
            Comment.objects.create(text=text, post=post, user=user, displayed_user=displayed_user, is_public=True)
        else:
            Comment.objects.create(text=text, post=post, user=user, displayed_user=displayed_user, is_public=False)
    return redirect('mysite:post_detail', pk=pk)
