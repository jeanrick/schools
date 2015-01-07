# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0002_auto_20150107_0452'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='school',
            field=models.ForeignKey(blank=True, to='grades.School', null=True),
            preserve_default=True,
        ),
    ]
