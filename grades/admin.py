from django.contrib import admin

from grades.models import Person, Address, Class, Subject, StudentGrade, StudentAssessment


admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(StudentGrade)
admin.site.register(StudentAssessment)
