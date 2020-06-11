from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

app_name = "mysite"

urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('top', TopView.as_view(), name='top'),
    path('post_index', PostIndexView.as_view(), name='post_index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/add_ajax', add_post_comment, name='add_post_comment'),
    path('category/<str:category_slug>/',
         CategoryIndexView.as_view(), name='category_index'),
    path("calendar", CalendarView.as_view(), name='calendar'),
    path('year_archive_index/<int:year>/', PostYearArchive.as_view(), name='post_year_archive'),
    path('month_archive_index/<int:year>/<int:month>/',
         PostMonthArchive.as_view(), name='post_month_archive'),
    path('circular_index', CircularIndexView.as_view(), name='circular_index'),
    path('event/<int:pk>/add_ajax/', add_event_join, name='add_event'),
    path('event/<int:pk>/remove_ajax/', remove_event_join, name='remove_event'),
    path('circular/<int:pk>/add_ajax/', add_circular_user, name='add_circular'),
    path('standard_index', StandardIndexView.as_view(), name='standard_index')
]
