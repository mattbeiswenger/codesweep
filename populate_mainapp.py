import datetime

assignments = {
    "Homework 1": {
        "points": 20,
        "description": "The parameter weekday is True if it is a \
        weekday, and the parameter vacation is True if we are on vacation. \
         We sleep in if it is not a weekday or we're on vacation. \
         Return True if we sleep in"
        "date": datetime.date(2012,9,16)
        "time":  datetime.time(5,45)
    }
    "Homework 2": {
        "points": 20,
        "description": "The parameter weekday is True if it is a \
        weekday, and the parameter vacation is True if we are on vacation. \
         We sleep in if it is not a weekday or we're on vacation. \
         Return True if we sleep in"
        "date": datetime.date(2012,9,16)
        "time":  datetime.time(5,45)
    }
}




title = models.CharField(max_length=128, unique=True)
points = models.IntegerField(default=0)
description = models.TextField()
date = models.DateField()
time = models.TimeField()

slug = models.SlugField(unique=True)

cats = {
        "Python": {"pages": python_pages,
        "likes": 64,
        "views": 128},
        "Django": {"pages": django_pages,
        "likes": 32,
        "views": 64},
        "Other Frameworks": {"pages": other_pages,
        "likes": 16,
        "views": 32}
    }
