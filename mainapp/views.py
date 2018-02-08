from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Assignment
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, JsonResponse

# modules for code submission
import os
import re
import datetime
from subprocess import Popen, PIPE
import shlex

# for debugging
import sys


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

        # retrieve data
        data = request.POST

        # create string for submitted code
        code = data['code_text']
        # remove beginning and end quotes
        code = code[1:-1]

        # create string for title
        assignment_title = data['assignment_title']
        # replace spaces with underscores
        assignment_title = assignment_title.replace(" ", "+")

        user = data['user']

        # date and time of submission
        currentDT = datetime.datetime.now()
        currentDT = currentDT.strftime("%Y-%m-%d--%H-%M-%S")

        # create unique filenames for code file and output file
        python_code_file = "{}--{}--{}.py".format(user, assignment_title, currentDT)
        code_output_file = "{}--{}--{}--outputs.py".format(user, assignment_title, currentDT)


        # un-escape backslash-escaped string
        code = bytes(code, "utf-8").decode("unicode_escape")

        # create path to downloads folder
        downloads_folder = ('/Users/matthewbeiswenger/Downloads')

        # create paths to individual files
        code_path = os.path.join(downloads_folder, python_code_file)
        input_path = os.path.join(downloads_folder, 'inputs.txt')
        expected_outputs_path = os.path.join(downloads_folder, 'expected--outputs.txt')

        # open files
        f = open(code_path, 'w')
        i = open(input_path, 'w')
        e = open(input_path, 'w')


        # write users code to the file
        f.write(code)

        function = Assignment.objects.get(title="Homework 1").function_name

        # import sys at top of file
        f.write("\n\n")
        f.write("import sys")

        # create sys Main() function
        f.write("\n\n")
        f.write("def Main():\n\t")
        f.write("with open(sys.argv[1], 'r') as input, " + \
            "open(sys.argv[2], 'w') as output:\n\t\t")
        f.write("for line in input:\n\t\t\t")
        f.write("output.write(str(" + function + "(int(line))) + '\\n')")
        f.write("\n\n")

        # create if __name__ == '__main__'
        f.write("if __name__ == '__main__':\n\tMain()")

        f.close()

        # retrieve the inputs from the assignment object with
        # the correlating assignment title
        inputs = Assignment.objects.get(title="Homework 1").inputs
        expected_outputs = Assignment.objects.get(title="Homework 1").outputs

        # write inputs to file
        i = open(input_path, 'w')
        for item in inputs:
            if item != "," and item != " ":
                i.write(item + '\n')
        i.close()

        # write expected outputs to file
        e = open(expected_outputs_path, 'w')
        for item in expected_outputs:
            if item != "," and item != " ":
                e.write(item + '\n')
        e.close()

        # execute the code
        os.chdir(downloads_folder)

        # take in file input
        # create file output and error file
        os.system('python3 ' + python_code_file + ' inputs.txt ' + \
        code_output_file + ' 2> error.txt')

        # read the error file
        with open('error.txt', 'r') as error_file:
            errorfile = error_file.readlines()[5:]
        errorfile = "".join(errorfile)

        with open(code_output_file, 'r') as output_file:
            outputfile = output_file.read()


        # create JSON data response
        data = {
            'error': errorfile,
            'output': outputfile
        }

        return JsonResponse(data)

    else:

        raise Http404()



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def user_login(request):

    if request.method == 'POST':

        # retrieve username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user
        user = authenticate(username=username, password=password)

        # if we have a User object, the details are correct
        # if None (Python's way of representing the absence of a value), no user
        # with matching credentials was found
        if user:

            # check that account is not disabled
            if user.is_active:

                # log the user in
                login(request, user)
                return assignments(request)
            else:

                # an inactive account was used
                return HttpResponse("Your account is disabled.")
        else:

            # no user credentials were found
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # the request is not a HTTP POST
    else:
        raise Http404()
