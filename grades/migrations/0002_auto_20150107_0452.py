# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'person'},
        ),
        migrations.RemoveField(
            model_name='school',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='school',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='school',
            name='parish',
        ),
        migrations.AddField(
            model_name='school',
            name='address',
            field=models.ForeignKey(blank=True, to='grades.Address', null=True),
            preserve_default=True,
        ),
    ]
