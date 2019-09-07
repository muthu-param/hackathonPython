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


class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    bookingDate = models.DateTimeField(auto_now=True, null=True)
    agenda = models.TextField(blank=True)
    historyState = models.IntegerField()

    class Meta:
        db_table = "booking"

class Blocking(models.Model):
    blockingId = models.AutoField(primary_key=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    bookingDate = models.DateTimeField(auto_now=True,null=True)
    status = models.IntegerField()

    class Meta:
        db_table = "blocking"

class MoM(models.Model):
    MoMId = models.AutoField(primary_key=True)
    bookingId = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    projectTitle = models.CharField(max_length=100)
    aboutMoM = models.CharField(max_length=300)
    remarks = models.CharField(max_length=100)
    submittingDate = models.DateTimeField(auto_now=True,null=True)
    sentiment = models.CharField(max_length=100, null=True)
    polarity = models.IntegerField(null=True)    

    class Meta:
        db_table = "mom"