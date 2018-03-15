import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
					'codesweep.settings')

import django
django.setup()

from mainapp.models import Assignment, InstructionFile, Term, Course
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta

def populate():



	students = [
		{"username": "kmalone",
		"password": "theoffice"},
		{"username": "jhalpert",
		"password": "theoffice"},
		{"username": "pbeesly",
		"password": "theoffice"},
	]

	faculty_members = [
		{"username": "mscott",
		"password": "theoffice"},
		{"username": "jlevinson",
		"password": "thoffice"},
	]

	terms = [
		{"season": "FA",
		"year": "2018"},
		{"season": "WI",
		"year": "2018"},
	]

	courses = [
		{"subject": "CSC",
		"number": "160",
		"section": "001",
		"professor": "mscott",
		"term_season": "FA",
		"term_year": "2018",
		"students": ["kmalone", "jhalpert"]},
		{"subject": "CSC",
		"number": "161",
		"section": "001",
		"professor": "jlevinson",
		"term_season": "WI",
		"term_year": "2018",
		"students": ["jhalpert", "pbeesly"]},
	]

	assignments = [
		{"title": "Double Char",
		"points": "10",
		"description": ("Given a string, return a string where for every char "
						"in the original, there are two chars.\n\n"
						"double_char('The') -> 'TThhee'\n"
						"double_char('AAbb') -> AAAAbbbb"),

		"date_due": datetime.today() + timedelta(days=7),
		"time_due": datetime.today() + timedelta(days=7),
		"inputs": "\"Codesweep\"\n\"LLAA\"",
		"outputs": "CCooddeesswweeeepp\nLLLLAAAA",
		"function_definition": "double_char(str)",
		"comment_to_code_ratio": "10",
		"slug": "Double+Char",
		"course_subject": "CSC",
		"course_number": "160",
		"course_section": "001"},
		{"title": "Sorta Sum",
		"points": "10",
		"description": ("Given two ints, a and b, return their sum. However, "
						"sums in the range 10...19 inclusive, are forbidden, "
						"so in that case just return 20.\n\n"
						"sorta_sum(3, 4) -> '7'\n"
						"sorta_sum(9, 4) -> 20"),

		"date_due": datetime.today() + timedelta(days=7),
		"time_due": datetime.today() + timedelta(days=7),
		"inputs": "14, 7\n9, 4\n-3, 12",
		"outputs": "21\n20\n9",
		"function_definition": "sorta_sum(a, b)",
		"comment_to_code_ratio": 10,
		"slug": "Sorta+Sum",
		"course_subject": "CSC",
		"course_number": "161",
		"course_section": "001"}
	]


	# create faculty group with permissions
	faculty_group, created = Group.objects.get_or_create(name='Faculty')

	content_type = ContentType.objects.get_for_model(Assignment)
	add_assignment = Permission.objects.get(name='Can add assignment')
	change_assignment = Permission.objects.get(name='Can change assignment')
	delete_assignment = Permission.objects.get(name='Can delete assignment')

	content_type = ContentType.objects.get_for_model(InstructionFile)
	add_instrfile = Permission.objects.get(name='Can add instruction file')
	change_instrfile = Permission.objects.get(name='Can change instruction file')
	delete_instrfile = Permission.objects.get(name='Can delete instruction file')

	faculty_group.permissions.add(
				add_assignment,
				change_assignment,
				delete_assignment,
				add_instrfile,
				change_instrfile,
				delete_instrfile
				)

	print("Created group: Faculty")

	# create student group
	student_group, created = Group.objects.get_or_create(name='Student')
	print("Created group: Student")


	# create admin
	User.objects.create_superuser(username="admin", password="password", email="")
	print("Created admin: username = admin, password = password")

	# create students
	for student in students:
		s = User.objects.create_user(username=student['username'], password=student['password'])
		student_group.user_set.add(s)
		print("Created student: username = " + student['username'] + ", password = " + student['password'])

	# create professors
	for fm in faculty_members:
		p = User.objects.create_user(username=fm['username'], password=fm['password'])
		faculty_group.user_set.add(p)
		print("Created professor: username = " + fm['username'] + ", password = " + fm['password'])

	# create terms
	for term in terms:
		Term.objects.get_or_create(season=term['season'], year=term['year'])[0]
		print("Created term: " + term['year'] + "/" + term['season'])

	# create courses
	for course in courses:
		p = User.objects.get(username=course['professor'])
		t = Term.objects.get(season=course['term_season'], year=course['term_year'])
		c, created = Course.objects.get_or_create(subject=course['subject'],
									number=course['number'],
									section=course['section'],
									professor=p,
									term=t)

		print("Created course: subject = {}, number = {}, section = {}, \
		+ professor = {}".format(course['subject'], course['number'],
									course['section'], course['professor'],))

		for student in course['students']:
			c.students.add(User.objects.get(username=student))
			print("Added student to course: " + student)

	# create assignments
	for assignment in assignments:
		c = Course.objects.get(subject=assignment['course_subject'],
								number=assignment['course_number'],
								section=assignment['course_section'])
		a, created = Assignment.objects.get_or_create(title=assignment['title'],
												description=assignment['description'],
												date_due=assignment['date_due'],
												time_due=assignment['time_due'],
												inputs=assignment['inputs'],
												outputs=assignment['outputs'],
												function_definition=assignment['function_definition'],
												comment_to_code_ratio=assignment['comment_to_code_ratio'],
												slug=assignment['slug'],
												course=c)

# start execution here
if __name__ == '__main__':
	print("Starting Codesweep population script...")
	populate()
