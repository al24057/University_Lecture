from django.db import models
import uuid
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="講義名")
    department = models.CharField(max_length=100, verbose_name="講義区分")
    credits = models.IntegerField(verbose_name="単位数")
    
    def __str__(self):
        return self.name

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=100, verbose_name="講師名")
    year = models.IntegerField()
    day_of_week = models.IntegerField(verbose_name="曜日", choices=[(0,"月曜"),(1,"火曜"),(2,"水曜"),(3,"木曜"),(4,"金曜"),(5,"土曜")])
    period = models.IntegerField()
    description = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.course
