from django.contrib import admin

from grades.models import Person, Address, School, Class, Subject, StudentGrade, AssessmentType, StudentAssessment, StudentAssessmentTypeWeight


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'number_of_students',)
    list_filter = ('address__parish',)


admin.site.register(Person)
admin.site.register(Address)
admin.site.register(School, SchoolAdmin)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(StudentGrade)
admin.site.register(StudentAssessment)
admin.site.register(StudentAssessmentTypeWeight)
admin.site.register(AssessmentType)
