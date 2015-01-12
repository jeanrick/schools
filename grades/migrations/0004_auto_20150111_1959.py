# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0003_person_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAssessmentTypeWeight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assessment_type', models.CharField(max_length=10, choices=[(b'Homework', b'Homework'), (b'Classwork', b'Classwork'), (b'Project', b'Project'), (b'Test', b'Test')])),
                ('weight', models.IntegerField(max_length=3)),
                ('required', models.BooleanField(default=False)),
                ('passing_percentage', models.IntegerField(null=True, blank=True)),
                ('subject', models.ForeignKey(to='grades.Subject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subject',
            name='passing_percentage',
            field=models.IntegerField(default=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='parish',
            field=models.CharField(max_length=20, choices=[(b'Trelawny', b'Trelawny'), (b'Hanover', b'Hanover'), (b'Kingston', b'Kingston'), (b'St. Andrew', b'St. Andrew'), (b'Westmoreland', b'Westmoreland')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='school',
            field=models.ForeignKey(related_name='persons', blank=True, to='grades.School', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='studentassessment',
            name='assessment_type',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
