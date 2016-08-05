from __future__ import unicode_literals

from django.db import models

TAG_CATEGORY_MOOD = "mood"
TAG_CATEGORY_GENRE = "genre"
TAG_CATEGORY_PLACE = "place"
TAG_CATEGORY_OTHER = "other"


class Tag(models.Model):
    category = models.CharField(max_length=25)
    name = models.CharField(max_length=50, unique=True)


class Playlist(models.Model):

    id = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(max_length=600, default="Description, yo")
    likes = models.IntegerField(default=0)
    user_id = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=100, default="")
    tags = models.ManyToManyField(Tag, through="TagInstance")


class TagInstance(models.Model):
    tag = models.ForeignKey(Tag)
    playlist = models.ForeignKey(Playlist)

