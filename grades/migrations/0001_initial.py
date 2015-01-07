# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line1', models.CharField(max_length=140)),
                ('line2', models.CharField(max_length=140, null=True, blank=True)),
                ('parish', models.CharField(max_length=20, choices=[(b'Trelawny', b'Trelawny'), (b'Hanover', b'Hanover'), (b'Westmoreland', b'Westmoreland'), (b'Kingston', b'Kingston'), (b'St. Andrew', b'St. Andrew')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('address1', models.CharField(max_length=140, null=True, blank=True)),
                ('address2', models.CharField(max_length=140, null=True, blank=True)),
                ('parish', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField(max_length=140, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assessment_type', models.CharField(max_length=10, choices=[(b'Homework', b'Homework'), (b'Classwork', b'Classwork'), (b'Project', b'Project'), (b'Test', b'Test')])),
                ('max_score', models.IntegerField()),
                ('time_given', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('participation_status', models.CharField(max_length=10, choices=[(b'Present', b'Present'), (b'Late', b'Late'), (b'Absent', b'Absent'), (b'Sick', b'Sick')])),
                ('assigned_at', models.DateTimeField()),
                ('assessment', models.ForeignKey(related_name='grades', to='grades.StudentAssessment')),
                ('assigned_by', models.ForeignKey(related_name='grades_assigned', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(related_name='grades', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_grades.userdetails_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='studentassessment',
            name='subject',
            field=models.ForeignKey(to='grades.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='school',
            field=models.ForeignKey(related_name='classes', to='grades.School'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='shift',
            field=models.ForeignKey(blank=True, to='grades.Shift', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='classes_attending', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(related_name='classes_taught', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.ForeignKey(blank=True, to='grades.Address', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
