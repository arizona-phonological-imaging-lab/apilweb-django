# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

#Mohsen: I've made some changes to the auto-generated file. Most importantly I deleted the PK lines,
#changed the FK lines, added related names, and deleted "_id" from FK names because apparently
#Django automatically appends it to whatever I put there.
from __future__ import unicode_literals

from django.db import models


class Experiment(models.Model):
    title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiment'


class ExperimentAssociation(models.Model):
    image = models.TextField(blank=True, null=True)  # This field type is a guess.
    experiment = models.ForeignKey(Experiment)

    class Meta:
        managed = False
        db_table = 'experiment_association'

class Word(models.Model):
    spelling = models.TextField(blank=True, null=True)
    segment_sequence = models.TextField(blank=True, null=True)
    segment_sequence = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'

class Segment(models.Model):
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    spelling = models.TextField(blank=True, null=True)
    detailed_spelling = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segment'

class Project(models.Model):
    title = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)  # This field type is a guess.
    folder_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'
        
class Video(models.Model):
    title = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project)
    duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    folder_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'

class Image(models.Model):
    end_word = models.ForeignKey(Word, related_name='end_word')
    start_word = models.ForeignKey(Word, related_name='start_word')
    word = models.ForeignKey(Word, related_name='word')
    end_segment = models.ForeignKey(Segment, related_name='end_segment')
    start_segment = models.ForeignKey(Segment, related_name='start_segment')
    segment = models.ForeignKey(Segment, related_name='segment')
    video = models.ForeignKey(Video)
    address = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    autotraced = models.TextField(blank=True, null=True)  # This field type is a guess.
    title = models.TextField(blank=True, null=True)
    is_bad = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'image'

class Tag(models.Model):
    image = models.ForeignKey(Image)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'
              
class Tracer(models.Model):
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracer'

class Trace(models.Model):
    approved = models.TextField(blank=True, null=True)  # This field type is a guess.
    address = models.TextField(blank=True, null=True)
    tracer = models.ForeignKey(Tracer)
    image = models.ForeignKey(Image)
    date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trace'




