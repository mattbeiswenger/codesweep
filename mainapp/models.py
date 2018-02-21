from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class InstructionFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(blank=True, null=True,
        upload_to='instructionfiles/%Y/%m/%d')

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=128, unique=True)
    points = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    date_due = models.DateField(blank=True)
    time_due = models.TimeField(blank=True)
    inputs = models.TextField()
    outputs = models.TextField()
    function_definition = models.CharField(max_length=128)
    comment_to_code_ratio = models.IntegerField(default=0, blank=True,
                    help_text="This number represents the percentage of \
                    characters that are within comments, compared to the \
                    entire body of code")
    slug = models.SlugField(unique=True)
    instruction_file = models.ManyToManyField(InstructionFile, blank=True)



    # slug feature
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, editable=False)
    file = models.FileField(blank=True, null=True, editable=False)
    date_submitted = models.DateField(blank=True)
    time_submitted = models.TimeField(blank=True)
    user = models.ForeignKey(User)
    correct = models.BooleanField(default=False)
    comment_ratio = models.IntegerField()

    def __FieldFile__(self):
        return self.file
