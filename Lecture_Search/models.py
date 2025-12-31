from django.db import models
import uuid

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="講義名")
    department = models.CharField(max_length=100, verbose_name="講義区分")
    credits = models.IntegerField(verbose_name="単位数")
    
    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="苗字")
    first_name = models.CharField(max_length=100, verbose_name="名前")
    full_name = models.CharField(max_length=200, verbose_name="フルネーム")
    
    def __str__(self):
        return self.full_name
    
class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    year = models.IntegerField()
    day_of_week = models.IntegerField(verbose_name="曜日", choices=[(0,"月曜"),(1,"火曜"),(2,"水曜"),(3,"木曜"),(4,"金曜"),(5,"土曜")])
    period = models.IntegerField()
    description = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.course
