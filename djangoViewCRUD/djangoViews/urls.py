from django.urls import path

from .views import (
    HomeView,
    DashboardView,
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
)

urlpatterns = [

    path("",HomeView.as_view(),name="home",),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
    path("students/",StudentListView.as_view(),name="student-list"),
    path("students/create/",StudentCreateView.as_view(),name="student-create"),
    path("students/<int:pk>/update/",StudentUpdateView.as_view(),name="student-update",),
    path("students/<int:pk>/delete/",StudentDeleteView.as_view(),name="student-delete",),
]