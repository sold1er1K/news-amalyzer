"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import news_analyzer.views as news_analyzer


urlpatterns = [
    path('', include('news_analyzer.urls', namespace='news_analyzer')),
    path('api/add-news/', news_analyzer.add_news, name='add_news'),
    path('api/analyze-news/', news_analyzer.analyze_news, name='analyze_news'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
