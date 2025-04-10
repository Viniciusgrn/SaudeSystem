from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/analytics', views.DashboardList.as_view(), name = "dashboard"),
]
