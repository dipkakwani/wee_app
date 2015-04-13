# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0002_auto_20150410_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(b'F', b'Following')])),
                ('userA', models.ForeignKey(related_name='Following.userA', to='userModule.User')),
                ('userB', models.ForeignKey(related_name='Following.userB', to='userModule.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(b'R', b'RequestSent'), (b'F', b'Friends')])),
                ('userA', models.ForeignKey(related_name='Friendship.userA', to='userModule.User')),
                ('userB', models.ForeignKey(related_name='Friendship.userB', to='userModule.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('userA', 'userB')]),
        ),
        migrations.AlterUniqueTogether(
            name='following',
            unique_together=set([('userA', 'userB')]),
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userid',
            new_name='userId',
        ),
    ]
