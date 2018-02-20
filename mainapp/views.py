from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Assignment, Submission
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.conf import settings

# modules for code submission
import os
import datetime
import re

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
    except Assignment.DoesNotExist:
        context_dict['assignment'] = None

    return render(request, 'mainapp/projectpage.html', context_dict)


def submit_text(request):

    if request.method == 'POST':


        data = request.POST # retrieve data

        code = data['code_text'] # obtain submitted code
        user = data['user'] # obtain the user submitting the code
        sys.stderr.write(repr(user) + '\n')
        assignment_title = data['assignment_title'] # obtain assignment title

        code = code[1:-1] # remove beginning and end quotes

        # retrieve data about this homework assignment from the db
        function = Assignment.objects.get(title=assignment_title).function_definition
        inputs = Assignment.objects.get(title=assignment_title).inputs
        expected_outputs = Assignment.objects.get(title=assignment_title).outputs


        # replace spaces with underscores
        # so the title can be used in a filename
        assignment_title = assignment_title.replace(" ", "+")




        # date and time of submission, to be used in filename
        currentDT = datetime.datetime.now()
        currentDT = currentDT.strftime("%Y-%m-%d--%H-%M-%S")

        # create unique filenames for code file and output file
        python_code_file = "{}--{}--{}.py".format(
                                user, assignment_title, currentDT)
        code_output_file = "{}--{}--{}--outputs.txt".format(
                                user, assignment_title, currentDT)


        # un-escape backslash-escaped code string
        code = bytes(code, "utf-8").decode("unicode_escape")

        # create path to downloads folder
        downloads_folder = ('/Users/matthewbeiswenger/Downloads')

        # create paths to individual files
        code_path = os.path.join(settings.MEDIA_ROOT, 'code', python_code_file)

        inputs_path = os.path.join(settings.MEDIA_ROOT, 'inputs', assignment_title, 'inputs.txt')
        sysargv_path = os.path.join(settings.STATIC_DIR, 'sysargv', 'sysargv.txt')
        expected_outputs_path = os.path.join(settings.MEDIA_ROOT, 'expectedoutputs', assignment_title, 'expected--outputs.txt')
        code_output_path = os.path.join('temp_files', 'code_output_files', code_output_file)

        # if the directories for the inputs path don't exist, make them
        os.makedirs(os.path.dirname(inputs_path), exist_ok=True)
        os.makedirs(os.path.dirname(expected_outputs_path), exist_ok=True)

        # create user's code file
        with open(code_path, 'w') as code_file, open(sysargv_path, 'r') as sysarg_file:
                code_file.write(code)
                code_file.write(sysarg_file.read())

        # create inputs file
        with open(inputs_path, 'w') as inputs_file:
            for item in inputs:
                if item != "," and item != " ":
                    inputs_file.write(item + '\n')

        # create expected outputs file
        with open(expected_outputs_path, 'w') as expected_outputs_file:
            for item in expected_outputs:
                if item != "," and item != " ":
                    expected_outputs_file.write(item + '\n')


        # take in file input
        # create outputs file and error file
        os.system('python3 {} {} {} 2> temp_files/error_files/error.txt'.format(code_path, inputs_path, code_output_path))

        os.system('diff -q {} {} > temp_files/diff_files/diff-results.txt'.format(code_output_path, expected_outputs_path))

        # read the error file
        with open('temp_files/error_files/error.txt', 'r') as error_file:
            # skip the lines relating to traceback to Main()
            errorfile = error_file.readlines()[5:]
        errorfile = "".join(errorfile)

        # read the outputs file
        with open(code_output_path, 'r') as output_file:
            outputfile = output_file.read()

        # read the outputs file
        with open('temp_files/diff_files/diff-results.txt', 'r') as diff_file:
            diff_results = diff_file.read()


        # --------- calculate code/comment ratio ------------- #

        # sum of comments
        # capture any characters between # and \n
        comments = re.findall(r"#.*\n|#.*", code)
        comments = str(comments)
        # remove erroneous characters
        comments = comments.replace("[", "")
        comments = comments.replace("]", "")
        comments = comments.replace("\\n", "")
        comments = comments.replace(" ", "")
        comments = comments.replace(",", "")
        comments = comments.replace("'", "")
        # sum characters in comment string
        comment_sum = 0
        for item in comments:
            comment_sum += 1

        # sum of code
        code = code.replace("\n", "")
        code = code.replace("\t", "")
        code_sum = 0
        for item in code:
            code_sum += 1

        comment_code_ratio = (comment_sum/code_sum)*100


        # ----------------------------------------------------- #

        correct = True
        if (diff_results):
            correct = False



        # -- obtain foreign fields from the db
        # obtain the db object for the current user
        current_user = User.objects.get(username=user)
        # change the assignment_title string so that it matches the
        # on in the database
        assignment_title = assignment_title.replace("+", " ")
        # obtain the db object for the current assignment
        current_assignment = Assignment.objects.get(title=assignment_title)

        # change the code path so that the server
        # can find it's address relative to the site's main page
        # if this wasn't changed, it would include the entire path
        # on the computer. For example, users/documents/python/codesweep/ etc...
        code_path = os.path.join('code', python_code_file)


        # create submission record
        submission = Submission()
        submission.user = current_user
        submission.assignment = current_assignment
        submission.file = code_path
        submission.date_submitted = datetime.datetime.now()
        submission.time_submitted = datetime.datetime.now()
        submission.correct = correct
        submission.comment_ratio = comment_code_ratio
        submission.save()


        # create JSON data response
        data = {
            'error': errorfile,
            'output': outputfile,
            'comment_ratio': comment_code_ratio,
            'diff_results': diff_results
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
