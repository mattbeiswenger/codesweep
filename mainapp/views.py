from django.shortcuts import render
from mainapp.models import Assignment

# Create your views here.


def login(request):
    return render(request, 'mainapp/login.html')

def hw(request):
    assignment_list = Assignment.objects.all()
    context_dict = {'assignments': assignment_list}
    return render(request, 'mainapp/homework.html', context_dict)
