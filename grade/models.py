from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from lesson.models import Lesson


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_student", verbose_name="Student", null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="grade_lesson", verbose_name="Lesson", null=True)
    grade = models.IntegerField(blank=True,verbose_name="Grade",null=True)
    date = models.DateField(blank=True,verbose_name="Date",null=True)
    description = models.CharField(max_length=160, blank=True,verbose_name="Description",null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_created_by", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_updated_by", null=True)

    def __str__(self):
        return "%s %s : %s" % (self.student.profile.name, self.student.profile.surname, self.grade)