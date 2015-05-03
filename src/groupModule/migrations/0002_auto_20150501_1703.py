# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupModule', '0001_initial'),
        ('userModule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joins',
            name='userId',
            field=models.ForeignKey(to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='joins',
            unique_together=set([('groupId', 'userId')]),
        ),
        migrations.AddField(
            model_name='group',
            name='adminId',
            field=models.ForeignKey(to='userModule.User'),
            preserve_default=True,
        ),
    ]
