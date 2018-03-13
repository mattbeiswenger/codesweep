from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class InstructionFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(blank=True, null=True,
        upload_to='instructionfiles/%Y/%m/%d')

    def __str__(self):
        return self.title


class Term(models.Model):
    FALL = 'FA'
    WINTER = 'WI'
    SPRING = 'SP'
    SEASON_CHOICES = (
        (FALL, 'Fall'),
        (WINTER, 'Winter'),
        (SPRING, 'Spring'),
    )
    season = models.CharField(
        max_length=2,
        choices=SEASON_CHOICES,
    )

    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return str(self.year) + "/" + self.season

    class Meta:
        ordering = ['year', 'season']


class Course(models.Model):
    subject = models.CharField(max_length=3)
    number = models.CharField(max_length=3)
    section = models.CharField(max_length=3)
    professor = models.ForeignKey("auth.User", limit_choices_to={'groups__name': "Faculty"}, related_name="faculty_profile", on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    students = models.ManyToManyField("auth.User", limit_choices_to={'groups__name': "Student"}, related_name="student_profile")

    def __str__(self):
        return '{}_{}_{}'.format(self.subject, self.number, self.section)

    class Meta:
        unique_together = ("subject", "number", "section")


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instruction_file = models.ManyToManyField(InstructionFile, blank=True)




    # slug feature
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, editable=False, on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, editable=False)
    date_submitted = models.DateField(blank=True)
    time_submitted = models.TimeField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    comment_ratio = models.IntegerField()

    def __FieldFile__(self):
        return self.file
