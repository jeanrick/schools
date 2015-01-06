from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
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

class Address(models.Model):
	line1 = models.CharField(max_length=140)
	line2 = models.CharField(max_length=140, null=True, blank=True)
	parish = models.CharField(max_length=20, choices=PARISH_CHOICES)

	def __unicode__(self):
		return u'{}, {}, {}'.format(self.line1, self.line2, self.parish)



# school
class School(models.Model):
	name = models.CharField(max_length=140)
	address1 = models.CharField(max_length=140, null=True, blank=True)
	address2 = models.CharField(max_length=140, null=True, blank=True)
	parish = models.CharField(max_length=20, choices=PARISH_CHOICES)


class Person(AbstractUser):
	address = models.ForeignKey('Address', null=True, blank=True)
	# details ... this is probably a polymorphic model
	# use Groups to determine if this person is a student etc

class UserDetails(PolymorphicModel):
	"""Extra data that we may need for a user"""
	pass



class Shift(models.Model):
	name = models.CharField(max_length=140)
	description = models.TextField(max_length=140, null=True, blank=True)

class Class(models.Model):
	school = models.ForeignKey("School", related_name="classes")
	name = models.CharField(max_length=140)
	shift = models.ForeignKey("Shift", null=True, blank=True)
	teacher = models.ForeignKey("Person", related_name="classes_taught")
	students = models.ManyToManyField("Person", related_name="classes_attending")


class Subject(models.Model):
	name = models.CharField(max_length=140)
	level = models.IntegerField()


class StudentGrade(models.Model):
	assessment = models.ForeignKey('StudentAssessment', related_name='grades')
	student = models.ForeignKey("Person", related_name='grades')
	score = models.IntegerField()
	participation_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
	# submitted_at?
	assigned_by = models.ForeignKey("Person", related_name='grades_assigned')
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
