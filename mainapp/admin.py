from django.contrib import admin
from mainapp.models import Assignment

# Register your models here.

class AssignmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Assignment, AssignmentAdmin)
