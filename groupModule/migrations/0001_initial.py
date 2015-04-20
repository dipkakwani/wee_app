# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('groupId', models.AutoField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=64)),
                ('groupType', models.CharField(max_length=1, choices=[(b'O', b'Open'), (b'C', b'Closed')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Joins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupId', models.ForeignKey(to='groupModule.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
