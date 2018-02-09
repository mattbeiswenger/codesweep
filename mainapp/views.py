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
    except Category.DoesNotExist:
        context_dict['assignment'] = None

    return render(request, 'mainapp/projectpage.html', context_dict)


def submit_text(request):

    if request.method == 'POST':


        data = request.POST # retrieve data

        code = data['code_text'] # obtain submitted code
        user = data['user'] # obtain the user submitting the code
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
        code_path = os.path.join(downloads_folder, python_code_file)
        inputs_path = os.path.join(downloads_folder, 'inputs.txt')
        expected_outputs_path = os.path.join(downloads_folder, 'expected--outputs.txt')

        # create user's code file
        with open(code_path, 'w') as code_file:
                # write users code to the file
                code_file.write(code)

                # import sys under user-submitted code
                code_file.write("\n\n")
                code_file.write("import sys")

                # create sys Main() function
                code_file.write("\n\n")
                code_file.write("def Main():\n\t")
                code_file.write("with open(sys.argv[1], 'r') as input, " + \
                    "open(sys.argv[2], 'w') as output:\n\t\t")
                code_file.write("for line in input:\n\t\t\t")
                code_file.write("output.write(str(" + function + \
                                "(int(line))) + '\\n')")
                code_file.write("\n\n")

                # create if __name__ == '__main__'
                code_file.write("if __name__ == '__main__':\n\tMain()")

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


        # execute the code
        os.chdir(downloads_folder)

        # take in file input
        # create outputs file and error file
        os.system('python3 ' + python_code_file + ' inputs.txt ' + \
        code_output_file + ' 2> error.txt')

        # read the error file
        with open('error.txt', 'r') as error_file:
            # skip the lines relating to traceback to Main()
            errorfile = error_file.readlines()[5:]
        errorfile = "".join(errorfile)

        # read the outputs file
        with open(code_output_file, 'r') as output_file:
            outputfile = output_file.read()


        # --------- calculate code/comment ratio ------------- #

        # sum of comments
        # capture any characters between # and \n
        comments = re.findall(r"#.*\n|#.*", code)
        comments = str(comments)
        # remove erroneous characters
        comments = comments.replace("[", "")
        comments = comments.replace("]", "")
        comments = comments.replace("\\n", "")
        comments = comments.replace("", "")
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

        # comment/code ratio in percentage form
        comment_code_ratio = "{0:.0f}%".format(comment_sum/code_sum * 100)

        # create JSON data response
        data = {
            'error': errorfile,
            'output': outputfile,
            'comment_ratio': comment_code_ratio
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
