from django.urls import path

from . import views

app_name = 'callNumberChecker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('output', views.OutputView.as_view(), name='output'),
    path('reset', views.ResetView.as_view(), name="reset")
]