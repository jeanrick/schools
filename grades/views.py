from datetime import date

from django.shortcuts import render

from grades.models import Person, StudentGrade

# Create your views here.

def report_sheet(request):
    """For now this just renders a demo report sheet for all students in the db"""
    grades = StudentGrade.objects.all()

    context = {
        'current_date': date.today(),
        'grades': grades,
    }
    return render(request, 'report_sheet.html', context)
