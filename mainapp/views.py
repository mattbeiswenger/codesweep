from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.views.decorators.http import (require_POST, require_GET,
                                        require_http_methods)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Assignment
from django.http import (Http404, HttpResponseNotFound, HttpResponseRedirect,
                        HttpResponse, HttpRequest)

# modules for code submission
import os
import subprocess

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
        data = data['code_text']
        # remove beginning and end quotes
        data = data[1:-1]


        # # decode data
        # data = request.body.decode('utf-8')
        #
        # # sys.stderr.write(repr(data) + '\n')
        #
        # data = urllib.parse.unquote(data)
        #
        # # sys.stderr.write(repr(data) + '\n')

        # data = data.split('"')
        # # replace spaces
        # data = data[1].replace('+', ' ')

        # ----- only allow escape characters in quotes ----- #

        data_list = data.split("'")

        sys.stderr.write(repr(data_list) + '\n')

        # replace newline
        data = data.replace('\\n', '\n')
        # replace tabs
        data = data.replace('\\t', '\t')



        # create path to downloads folder
        downloads_folder = ('/Users/matthewbeiswenger/Downloads')

        # create paths to individual files
        code_path = os.path.join(downloads_folder, 'codetext.py')
        input_path = os.path.join(downloads_folder, 'input.txt')

        # open files
        f = open(code_path, 'w')
        i = open(input_path, 'w')

        # import sys at top of file
        f.write("import sys")
        f.write("\n\n")

        # write users code to the file
        f.write(data)

        function = Assignment.objects.get(title="Homework 1").function_name
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

        # write inputs to file
        i = open(input_path, 'w')
        for item in inputs:
            if item != "," and item != " ":
                i.write(item + '\n')
        i.close()


        # execute the code
        os.chdir(downloads_folder)
        os.system('python3 codetext.py input.txt output.txt')

        return HttpResponse("Code has executed")

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
