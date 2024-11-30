from django.urls import path
from . import views

app_name = 'news_analyzer'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('history', views.history_page, name='history_page'),
]