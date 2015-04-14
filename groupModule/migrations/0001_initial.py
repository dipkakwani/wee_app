# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0003_auto_20150413_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('groupId', models.AutoField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=64)),
                ('adminId', models.ForeignKey(to='userModule.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Joined',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupId', models.ForeignKey(to='groupModule.Group')),
                ('userId', models.ForeignKey(to='userModule.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postId', models.AutoField(serialize=False, primary_key=True)),
                ('privacy', models.CharField(max_length=1, choices=[(b'L', b'Limited'), (b'P', b'Public')])),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('likes', models.BigIntegerField(default=0)),
                ('comments', models.BigIntegerField(default=0)),
                ('shares', models.BigIntegerField(default=0)),
                ('content', models.TextField()),
                ('groupId', models.ForeignKey(to='groupModule.Group', null=True)),
                ('posterId', models.ForeignKey(to='userModule.User')),
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
    ]
