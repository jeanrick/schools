# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import schools.utils


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0004_auto_20150111_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(related_name='subjects_taught', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='term',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='year',
            field=models.IntegerField(default=schools.utils.get_current_year),
            preserve_default=True,
        ),
    ]
