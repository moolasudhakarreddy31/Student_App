from email.policy import default
from django.db import models
from django.contrib.auth.models import User

class StudentSubjects(models.TextChoices):
    Total = 'Total Marks'
    Maths = 'Maths'
    Physics = 'Physics'
    English = 'English'

class Student(models.Model):
    name = models.CharField(max_length=25)
    roll_no= models.PositiveBigIntegerField(null=True, blank = True)
    subject = models.CharField(max_length=25, choices=StudentSubjects.choices, default=StudentSubjects.Total)
    marks = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now_add=True)

    class Meta:
        verbose_name="Students Created"