# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'experiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExperimentAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('image_id', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'experiment_association',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('autotraced', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('is_bad', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'image',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('language', models.TextField(blank=True, null=True)),
                ('folder_address', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.TextField(blank=True, null=True)),
                ('spelling', models.TextField(blank=True, null=True)),
                ('detailed_spelling', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'segment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('approved', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'trace',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tracer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tracer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('duration', models.TextField(blank=True, null=True)),
                ('folder_address', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('spelling', models.TextField(blank=True, null=True)),
                ('segment_sequence', models.TextField(blank=True, null=True)),
                ('segment_id_sequence', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'word',
                'managed': False,
            },
        ),
    ]
