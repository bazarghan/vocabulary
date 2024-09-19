import uuid

from django.db import models


class Vocabulary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word_name = models.CharField(max_length=255, unique=True)
    american_phonetic = models.CharField(max_length=255, null=True, blank=True)
    british_phonetic = models.CharField(max_length=255, null=True, blank=True)
    american_audio_url = models.URLField(null=True, blank=True)
    british_audio_url = models.URLField(null=True, blank=True)
    short_definition = models.TextField(null=True, blank=True)
    long_definition = models.TextField(null=True, blank=True)
    persian_definition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.word_name


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    part_of_speech = models.CharField(max_length=255)
    type = models.CharField(max_length=3)
    definition = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.word.word_name
