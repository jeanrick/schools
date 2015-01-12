from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from polymorphic import PolymorphicModel

from grades import constants
from schools.utils import get_current_year

PARISHES = [
	"Trelawny",
	"Hanover",
	"Kingston",
	"St. Andrew",
	"Westmoreland",
]
PARISH_CHOICES = ((parish, parish) for parish in PARISHES)

ATTENDANCES = [
	"Present",
	"Late",
	"Absent",
	"Sick",
]
ATTENDANCE_CHOICES = ((attendance, attendance) for attendance in ATTENDANCES)

TEACHERS_GROUP = 'Teachers'
PRINCIPALS_GROUP = 'Principals'
SENIOR_TEACHERS_GROUP = 'Senior Teachers'
STUDENTS_GROUP = 'Students'


class Address(models.Model):
	line1 = models.CharField(max_length=140)
	line2 = models.CharField(max_length=140, null=True, blank=True)
	parish = models.CharField(max_length=20, choices=PARISH_CHOICES)

	def __unicode__(self):
		return u'{}, {}, {}'.format(self.line1, self.line2, self.parish)



# school
class School(models.Model):
	name = models.CharField(max_length=140)
	address = models.ForeignKey('Address', null=True, blank=True)

	def __unicode__(self):
		return u'{}'.format(self.name)

	@property
	def staff_members(self):
		staff_groups = [
			TEACHERS_GROUP,
			SENIOR_TEACHERS_GROUP,
			PRINCIPALS_GROUP,
		]
		return self.persons.filter(groups__in=Group.objects.filter(name__in=staff_groups))

	@property
	def number_of_staff_members(self):
		return self.staff_members.count()

	@property
	def students(self):
		return self.persons.filter(groups__in=Group.objects.filter(name=STUDENTS_GROUP))

	@property
	def number_of_students(self):
		return self.students.count()


class Person(AbstractUser):
	TEACHER = 'Teacher'
	STUDENT = 'Student'

	class Meta:
		verbose_name = 'person'

	# use Groups to determine if this person is a student etc
	address = models.ForeignKey('Address', null=True, blank=True)
	# extra_details ... this is probably a polymorphic model
	school = models.ForeignKey('School', null=True, blank=True, related_name='persons')

	def __unicode__(self):
		user_type = 'Teacher' if self.is_teacher else 'Student'
		return u'{} {} ({})'.format(self.first_name, self.last_name, user_type)

	@property
	def is_teacher(self):
		return self.groups.filter(name=TEACHERS_GROUP).exists()

	@property
	def is_student(self):
		return self.groups.filter(name=STUDENTS_GROUP).exists()

	def generate_report_sheet(self, subjects):
		"""Return a dictionary containing the all grades for the given subjects formatted
		for use in a report sheet"""
		if self.is_student:
			report_sheet = []
			# For each subject, find all student assessments
			for subject in subjects:
				subject_data = {
					'subject': subject.name
				}
				subject_grades = {}
				assessment_types = AssessmentType.objects.filter(student_assessments__subject=subject).annotate(
					number=models.Count('student_assessments'), max_score=models.Sum('student_assessments__max_score'))
				for assessment_type in assessment_types:
					# Probably will optimize this later, but ...
					type_weight = StudentAssessmentTypeWeight.objects.filter(subject=subject, assessment_type=assessment_type)[0]
					subject_grades[assessment_type.name] = {
						'max_score': assessment_type.max_score,
						'actual_score': 0,
						'max_percentage': type_weight.weight,
						'actual_percentage': 0,
					}
					assessments = subject.student_assessments.filter(assessment_type=assessment_type)
					for assessment in assessments:
						# Assuming only one grade for now
						student_grade = assessment.grades.filter(student=self)[0]
						subject_grades[assessment_type.name]['actual_score'] += student_grade.score
					actual_score = subject_grades[assessment_type.name]['actual_score']
					max_score = subject_grades[assessment_type.name]['max_score']
					max_percentage = type_weight.weight
					subject_grades[assessment_type.name]['actual_percentage'] = (float(actual_score)/max_score)*max_percentage
				subject_data['grades'] = subject_grades
				report_sheet.append(subject_data)
			# Use final grades to to determine score out of (weight) for each type
			# Determine final grade for the subject
			# Determine final grade (average) overall
			print('Generated report sheet: {}'.format(report_sheet))
			return report_sheet
		else:
			print('Cannot generate a report sheet for a non-student')



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

	def __unicode__(self):
		return u'{} - {}'.format(self.name, self.teacher)



# This is where things get weird ... we need Instances and Definitions to be separate
# A subject in one year is not the same as a subject in another. Also, we need to
# keep track of which subject was taught by whom in which class/term etc

class Subject(models.Model):
	name = models.CharField(max_length=140)
	level = models.IntegerField()
	passing_percentage = models.IntegerField()
	year = models.IntegerField(default=get_current_year)
	term = models.IntegerField(default=1)
	# If this is blank  then use the teacher of the class
	teacher = models.ForeignKey('Person', related_name='subjects_taught', blank=True, null=True)

	def __unicode__(self):
		return u'{} (Level {})'.format(self.name, self.level)


class AssessmentType(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=140, blank=True, null=True)

	def __unicode__(self):
		return u'{}'.format(self.name)


class StudentAssessmentTypeWeight(models.Model):
	assessment_type = models.ForeignKey('AssessmentType', related_name='student_assessment_weights')
	subject = models.ForeignKey('Subject')
	# Percentage that this assessment type accounds for in the subject. If all the
	# weights on a subject do not add up to 100 then the weights are used as a ratio
	# to find the percentage out of 100
	weight = models.IntegerField(max_length=3)
	# If an assessment type is required, if a student fails to pass the assessment
	# he/she fails the entire subject
	required = models.BooleanField(default=False)
	passing_percentage = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return u'{} {} - {}% (Required: {})'.format(self.subject, self.assessment_type, self.weight, self.required)



class StudentGrade(models.Model):
	assessment = models.ForeignKey('StudentAssessment', related_name='grades')
	student = models.ForeignKey("Person", related_name='grades')
	score = models.IntegerField()
	participation_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
	# submitted_at?
	assigned_by = models.ForeignKey("Person", related_name='grades_assigned')
	assigned_at = models.DateTimeField()

	def __unicode__(self):
		return u'{}: {} - {}/{}'.format(self.assessment, self.student, self.score, self.assessment.max_score)

	# may need to override save to check that the given grade is allowed



class StudentAssessment(models.Model):
	subject = models.ForeignKey("Subject", related_name='student_assessments')
	assessment_type = models.ForeignKey('AssessmentType', related_name='student_assessments')
	max_score = models.IntegerField()
	time_given = models.DateTimeField(default=datetime.now)
	# time_due?

	def __unicode__(self):
		return u'{} for {} given on {}'.format(self.assessment_type, self.subject, self.time_given.date())
