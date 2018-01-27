from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=128, unique=True)
    points = models.IntegerField(default=0)
    description = models.TextField()
    due_date = models.DateField()
    time = models.TimeField()
    inputs = models.TextField()
    function_name = models.CharField(max_length=128)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Assignment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):

    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username
