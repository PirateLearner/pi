# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-28 16:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('data', models.TextField()),
                ('published_flag', models.BooleanField(default=0, verbose_name=b'is published?')),
                ('special_flag', models.BooleanField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name=b'date modified')),
                ('url_path', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=100)),
                ('publication_start', models.DateTimeField(default=django.utils.timezone.now, help_text=b'Used for automatic delayed publication. For this feature to work published_flag must be on.', verbose_name=b'Published Since')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogcontent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publication_start'],
            },
        ),
        migrations.CreateModel(
            name='BlogContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=100, unique=True)),
                ('is_leaf', models.BooleanField(default=0, verbose_name=b'Is leaf node?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('data', models.TextField()),
                ('slug', models.SlugField()),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogging.BlogContentType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='blogging.BlogParent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogcontent',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogging.BlogContentType'),
        ),
        migrations.AddField(
            model_name='blogcontent',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogging.BlogParent'),
        ),
        migrations.AddField(
            model_name='blogcontent',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
