from django.shortcuts import render
from mainapp.models import Assignment
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Assignment
from django.http import Http404, HttpResponseNotFound
import os
import json
# for debugging
import sys
import urllib.parse


# Create your views here.


def index(request):
    return render(request, 'mainapp/login.html')

@login_required
def assignments(request):
    assignment_list = Assignment.objects.all()
    context_dict = {'assignments': assignment_list}
    return render(request, 'mainapp/assignments.html', context_dict)

@login_required
def show_assignment(request, assignment_name_slug):
    try:
        context_dict = {}
        assignment = Assignment.objects.get(slug=assignment_name_slug)
        context_dict['assignment'] = assignment
    except Category.DoesNotExist:
        context_dict['assignment'] = None

    return render(request, 'mainapp/projectpage.html', context_dict)


def submit_text(request):

    if request.method == 'POST':

        data = request.body.decode('utf-8')
        data = urllib.parse.unquote(data)

        data = data.split('"')
        # replace spaces
        data = data[1].replace('+', ' ')
        # replace newline
        data = data.replace('\\n', '\n')
        # replace tabs
        data = data.replace('\\t', '\t')

        # sys.stderr.write(repr(data) + '\n')

        # create path to downloads folder
        downloads_folder = ('/Users/matthewbeiswenger/Downloads')

        # create paths to individual files
        code_path = os.path.join(downloads_folder, 'codetext.py')
        input_path = os.path.join(downloads_folder, 'input.txt')
        output_path = os.path.join(downloads_folder, 'output.txt')

        # open files
        f = open(code_path, 'w')
        i = open(input_path, 'w')

        # import sys at top of file
        f.write("import sys")
        f.write("\n\n")

        # write users code to the file
        f.write(data)

        # create sys Main() function
        f.write("\n\n")
        f.write("def Main():\n\t")
        f.write("with open(sys.argv[1], 'r') as input, " + \
            "open(sys.argv[2], 'w') as output:\n\t\t")
        f.write("for line in input:\n\t\t\t")
        f.write("output.write(str(fib(int(line))) + '\\n')")
        f.write("\n\n")


        f.write("if __name__ == '__main__':\n\tMain()")

        f.close()
        # retrieve the inputs from the assignment object with
        # the correlating assignment title
        inputs = Assignment.objects.get(title="Homework 1").inputs

        # write inputs to file
        i = open(input_path, 'w')
        for item in inputs:
            if item != "," and item != " ":
                i.write(item + '\n')
        i.close()


        # execute the code
        os.chdir(downloads_folder)
        os.system('python3 codetext.py input.txt output.txt')


        return HttpResponse("Hello")
    else:
        raise Http404()





@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)

                return assignments(request)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
                # The request is not a HTTP POST, so display the login form.
                # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        raise Http404()
