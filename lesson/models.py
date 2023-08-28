from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone



class Lesson(models.Model):
    name = models.CharField(max_length=80, blank=True,verbose_name="Name",null=True)
    description = models.CharField(max_length=160, blank=True,verbose_name="Description",null=True)
    period = models.CharField(max_length=32, blank=True,verbose_name="Period",null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_teacher", verbose_name="Teacher", null=True)
    students = models.ManyToManyField(User, related_name="lesson_students", verbose_name="Students", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_created_by", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_updated_by", null=True)

    def __str__(self):
        return "%s %s" % (self.name, self.description)