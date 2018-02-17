from django.contrib import admin
from mainapp.models import Assignment, UserProfile, InstructionFile, Submission

# Register your models here.

class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment', 'file', 'date_submitted',
        'time_submitted', 'correct', 'comment_ratio')
    # assignment = models.ForeignKey(Assignment)
    # file = models.FileField(blank=True, null=True,
    #      upload_to='submitted_files/')
    # date_submitted = models.DateField(blank=True)
    # time_submitted = models.TimeField(blank=True)
    # user = models.ForeignKey(UserProfile, editable=False)
    # correct = models.BooleanField(default=False)
    # comment_ratio = models.IntegerField()

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(UserProfile)
admin.site.register(InstructionFile)
admin.site.register(Submission, SubmissionAdmin)
