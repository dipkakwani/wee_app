# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userModule.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(unique=True, max_length=40)),
                ('password', models.CharField(max_length=256)),
                ('dob', models.DateField()),
                ('sex', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('description', models.CharField(default=b'', max_length=160, blank=True)),
                ('profilePic', models.ImageField(default=userModule.models.defaultImage, upload_to=userModule.models.getImagePath)),
                ('school', models.CharField(default=b'', max_length=50, blank=True)),
                ('college', models.CharField(default=b'', max_length=50, blank=True)),
                ('companyName', models.CharField(default=b'', max_length=50, blank=True)),
                ('status', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'S', b'Single'), (b'M', b'Married'), (b'', b'Unkown')])),
                ('profession', models.CharField(default=b'', max_length=30, blank=True)),
                ('website', models.URLField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
