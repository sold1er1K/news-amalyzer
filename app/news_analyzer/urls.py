from django.urls import path
from . import views

app_name = 'news_analyzer'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('history', views.history_page, name='history_page'),
    path('analytics', views.analytics_page, name='analytics_page'),
    path('analytics/distribution-diagram/', views.distribution_diagram, name='distribution_diagram'),
    path('analytics/dynamics-diagram/', views.dynamics_diagram, name='dynamics_diagram'),
    path('history/<int:news_id>/', views.news_detail, name='news_detail'),
]