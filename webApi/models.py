# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from enum import Enum


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.CharField(default=None, null=True, max_length=50)
    status = models.CharField(max_length=10)
    createdBy = models.CharField(max_length=10, default=None)
    role = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user"

class Role(models.Model):
    roleId = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=50)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = "role"

class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    roomName = models.CharField(max_length=200)
    size = models.IntegerField()
    utilityAC = models.BooleanField()
    utilitySmTv = models.BooleanField()
    utilityWater = models.BooleanField()
    utilityWBoard = models.BooleanField()
    utilityProjector = models.BooleanField()
    createdBy = models.CharField(max_length=10, default=None)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = "room"

