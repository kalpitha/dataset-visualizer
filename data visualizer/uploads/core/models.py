from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Dashboard(models.Model):
	phrase = models.BooleanField(default=False)
	sentence = models.CharField(max_length=300,primary_key=True)
	photography = models.BooleanField(default=False)
	travel = models.BooleanField(default=False)
	diy = models.BooleanField(default=False)
	fitness = models.BooleanField(default=False)
	food = models.BooleanField(default=False)
	extreme = models.BooleanField(default=False)
	sport = models.BooleanField(default=False)


class Entity(models.Model):
	text = models.ForeignKey(Dashboard,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	value = models.CharField(max_length=50)
	startval = models.PositiveIntegerField()
	endval = models.PositiveIntegerField()

