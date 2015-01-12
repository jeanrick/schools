from pprint import pprint

from django.test import TestCase
from django.core.management import call_command

from grades.models import Person, Subject

# Create your tests here.

class GradesTestCase(TestCase):

    def setUp(self):
        print('Trying to load data manually')
        call_command('loaddata', 'test_data')
        call_command('loaddata', 'test_data_auth')
        # fixtures = ['grades/fixtures/initial_data.json']

    def test_generate_report_sheet_data(self):
        """Tests that a data dictionary is generated for a student given a list
        or queryset of subjects"""

        print('All persons: {}'.format(Person.objects.all()))
        jane = Person.objects.all()[1]
        print(jane)
        report = jane.generate_report_sheet(Subject.objects.all())
        pprint(report)
