from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Assignment(models.Model):
    title = models.CharField(max_length=128, unique=True)
    points = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    date_due = models.DateField(blank=True)
    time_due = models.TimeField(blank=True)
    inputs = models.TextField()
    outputs = models.TextField()
    function_definition = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    instructions_file = models.FileField(blank=True, null=True,
        upload_to='instruction_files/%Y/%m/%d')

    # slug feature
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username
