from django.contrib import admin
from mainapp.models import Assignment, UserProfile, InstructionFile, Submission

# Register your models here.

class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'file', 'date_submitted',
        'time_submitted', 'correct', 'comment_ratio')

    readonly_fields=('user', 'assignment', 'file', 'date_submitted',
        'time_submitted', 'correct', 'comment_ratio')


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(UserProfile)
admin.site.register(InstructionFile)
admin.site.register(Submission, SubmissionAdmin)
