from django.contrib import admin
from mainapp.models import Assignment, InstructionFile, Submission
from mainapp.models import Course, Term


class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'file', 'date_submitted',
        'time_submitted', 'correct', 'comment_ratio')

    readonly_fields=('user', 'assignment', 'file', 'date_submitted',
        'time_submitted', 'correct', 'comment_ratio')

    list_filter = ('user', 'assignment', 'correct')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_subject', 'course_number', 'section_id', 'term')



admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(InstructionFile)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Term)
