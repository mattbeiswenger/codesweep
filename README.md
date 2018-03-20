# Abstract
This project was created for an Independent Study at North Central College during Winter 2018 term.

The purpose of this project is to establish a proof of concept for an intelligent grading system for introductory computer science courses, analyzing code through both static and dynamic procedures in order to provide useful feedback for both students and professors. This intelligent grading system is presented through a web application that allows for users to gain access through any modern web browser. At the core of the web application lies client-server communication that enables users to execute and submit source code. The outputs of the source code are then graded in relation to desired results that are specified by the professor. In the process of creating this project, many security issues were made apparent, including the security implications of running arbitrary code and the difficulties of sandboxing programming languages.

## Technologies Utilized
- Python/Django
- CSS/Bootstrap
- Javascript/JQuery
- JSON
- Ajax

# Installation for Testing
Assuming that Python 3.0, pip, and git are installed on your computer, perform the following steps:

1. Install Django with pip3 -
`pip3 install django`

2. Clone this repository in the desired folder -
`git clone https://github.com/mbeiswenger/codesweep`

3. Within the codesweep project directory, migrate the database -
`python3 manage.py migrate`

4. Populate the database with the population script -
`python3 populate-codesweep.py`

5. Run Django's local server -
`python3 manage.py runserver`

# To Be Implemented
- [x] Update the assignments shown when student clicks on a course in the list group
- [ ] Create slugs for term and course so that assignments can have the same name
- [ ] Display whether or not the current user has completed the assignment
- [ ] Provide option for students to look at history of submitted code
- [ ] Allow professors to hide his or her assignment until specified date and time
- [ ] Create submit button rather than uploading executed code
- [ ] Allow professors to download student code files in bulk
- [ ] Create temporary file feature for files created but never placed in the database
- [ ] Display correctness for each test case instead of displaying a binary value of either 'correct' or 'incorrect'
- [ ] Display badge on course list group showing number of uncompleted assignments
- [ ] Utilize AJAX for login authentication
