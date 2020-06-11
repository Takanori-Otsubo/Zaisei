from django.urls import path
from .views import CoronaVirusView

app_name = "questionnaire"

urlpatterns = [
    path('CoronaVirus', CoronaVirusView.as_view(), name='CoronaVirus'),
]
