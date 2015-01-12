# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0005_auto_20150112_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=140, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='studentassessment',
            name='assessment_type',
            field=models.ForeignKey(to='grades.AssessmentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='studentassessmenttypeweight',
            name='assessment_type',
            field=models.ForeignKey(to='grades.AssessmentType'),
            preserve_default=True,
        ),
    ]
