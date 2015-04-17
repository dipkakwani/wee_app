# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userModule.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groupModule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=140)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('originalPostId', models.ForeignKey(to='userModule.Post')),
                ('postId', models.ForeignKey(related_name='Share.postId', to='userModule.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(unique=True, max_length=40)),
                ('password', models.CharField(max_length=70)),
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
        migrations.AddField(
            model_name='share',
            name='userId',
            field=models.ForeignKey(related_name='Share.userId', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([('userId', 'postId')]),
        ),
        migrations.AddField(
            model_name='post',
            name='posterId',
            field=models.ForeignKey(to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='postId',
            field=models.ForeignKey(related_name='Like.postId', to='userModule.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='userId',
            field=models.ForeignKey(related_name='Like.userId', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('userId', 'postId')]),
        ),
        migrations.AddField(
            model_name='friendship',
            name='userA',
            field=models.ForeignKey(related_name='Friendship.userA', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friendship',
            name='userB',
            field=models.ForeignKey(related_name='Friendship.userB', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('userA', 'userB')]),
        ),
        migrations.AddField(
            model_name='following',
            name='userA',
            field=models.ForeignKey(related_name='Following.userA', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='userB',
            field=models.ForeignKey(related_name='Following.userB', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='following',
            unique_together=set([('userA', 'userB')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='postId',
            field=models.ForeignKey(related_name='Comment.postId', to='userModule.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='userId',
            field=models.ForeignKey(related_name='Comment.userId', to='userModule.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('userId', 'postId')]),
        ),
    ]
