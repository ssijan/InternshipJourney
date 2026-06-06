from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Student


# Django view
class HomeView(View):

    def get(self, request):

        return render(request, 'wc.html')


    

# django tamplateView

class DashboardView(TemplateView):

    template_name = "home.html"



# djnago ListView, CreateView, UpdateView, DeleteView

class StudentListView(ListView):

    model = Student

    template_name = "student_list.html"

    context_object_name = "students"



class StudentCreateView(CreateView):

    model = Student

    fields = [
        "name",
        "email",
        "department",
        "cgpa",
    ]

    template_name = "student_form.html"

    success_url = reverse_lazy("student-list")



class StudentUpdateView(UpdateView):

    model = Student

    fields = [
        "name",
        "email",
        "department",
        "cgpa",
    ]

    template_name = "student_form.html"

    success_url = reverse_lazy("student-list")



class StudentDeleteView(DeleteView):

    model = Student

    template_name = "student_confirm_delete.html"

    success_url = reverse_lazy("student-list")