from django.shortcuts import render
from mainapp.models import Assignment

# Create your views here.


def login(request):
    return render(request, 'mainapp/login.html')

def hw(request):
    assignment_list = Assignment.objects.all()
    context_dict = {'assignments': assignment_list}
    return render(request, 'mainapp/homework.html', context_dict)

def show_assignment(request, assignment_name_slug):
    try:
        context_dict = {}
        assignment = Assignment.objects.get(slug=assignment_name_slug)
        context_dict['assignment'] = assignment
    except Category.DoesNotExist:
        context_dict['assignment'] = None

    return render(request, 'mainapp/projectpage.html', context_dict)
