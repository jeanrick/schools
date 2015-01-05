from datetime import datetime

from django.db import models
from polymorphic import PolymorphicModel

PARISHES = [
	"Trelawny",
	"Hanover",
	"Westmoreland",
	"Kingston",
	"St. Andrew",
]
PARISH_CHOICES = ((parish, parish) for parish in PARISHES)

ATTENDANCES = [
	"Present",
	"Late",
	"Absent",
	"Sick",
]
ATTENDANCE_CHOICES = ((attendance, attendance) for attendance in ATTENDANCES)

# school
class School(models.Model):
	name = models.CharField(max_length=140)
	address1 = models.CharField(max_length=140, null=True, blank=True)
	address2 = models.CharField(max_length=140, null=True, blank=True)
	parish = models.CharField(max_length=20, choices=PARISH_CHOICES)

class Person(PolymorphicModel):
	pass

class Teacher(Person):
	pass

class Student(Person):
	pass


class Shift(models.Model):
	name = models.CharField(max_length=140)
	description = models.TextField(max_length=140, null=True, blank=True)

class Class(models.Model):
	school = models.ForeignKey("School", related_name="classes")
	name = models.CharField(max_length=140)
	shift = models.ForeignKey("Shift", null=True, blank=True)
	teacher = models.ForeignKey("Teacher", related_name="classes")
	students = models.ManyToManyField("Student", related_name="classes")

class Subject(models.Model):
	name = models.CharField(max_length=140)
	level = models.IntegerField()

class StudentGrade(models.Model):
	assessment = models.ForeignKey('StudentAssessment', related_name='grades')
	student = models.ForeignKey("Student")
	score = models.IntegerField()
	participation_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
	# submitted_at?
	assigned_by = models.ForeignKey("Teacher")
	assigned_at = models.DateTimeField()

class StudentAssessment(models.Model):
	ASSESSMENT_TYPES = [
		"Homework",
		"Classwork",
		"Project",
		"Test",
	]
	ASSESSMENT_CHOICES = ((assessment_type, assessment_type) for assessment_type in ASSESSMENT_TYPES)
	subject = models.ForeignKey("Subject")
	assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_CHOICES)
	max_score = models.IntegerField()
	time_given = models.DateTimeField(default=datetime.now)
	# time_due?
