"""Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('search/', views.search),
    path('tender/', views.tender),
    path('searchbycompany/', views.searchbycompany),
    path('searchbyid/', views.searchbyid),
    path('unit/', views.unit),
    path('date/', views.date),
    path('analytic/', views.analytic),
    path('analyticid/', views.analyticid),
    path('comdata/', views.comdata),
    path('comdataid/', views.comdataid),
    path('tendsearch/', views.tendsearch),
    path('test/', views.test),
    path('predict/',views.predict),
    path('competitor/',views.competitor),
    path('analytic2/',views.analytic2),
    path('example/',views.example)
]
