# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Booking
from webApi.models import User
from webApi.services import sendMail


def index(request):
    try:
        res = {}
        res['status'] = 200
        res['message'] = 'Working Fine...!'
        return success_response(res)
    except Exception as e:
        return failure_response(e.message)

@api_view(['POST'])
def addBooking(roomId,userId,start,end,date,agenda):
    fail = {}
    responses = {}
    data = json.loads(request.body.decode('utf-8'))

    if 'roomId' not in data:
        fail['msg'] = "Please provide room id"
        return failure_response(fail)
    elif 'userId' not in data:
        fail['msg'] = "Please provide user id"
        return failure_response(fail)
    elif 'startTime' not in data:
        fail['msg'] = "Please provide start time"
        return failure_response(fail)
    elif 'end time' not in data:
        fail['msg'] = "Please provide end time"
        return failure_response(fail)
    elif 'bookingDate' not in data:
        fail['msg'] = "Please provide booking date"
        return failure_response(fail)
    elif 'agenda' not in data:
        fail['msg'] = "Please provide agenda"
        return failure_response(fail)

    booking = Booking()
    booking.roomId = data['roomId']
    booking.userId = data['userId']
    booking.startTime = data['startTime']
    booking.endTime = data['endTime']
    booking.bookingDate = data['bookingDate']
    booking.agenda = data['agenda'] 
    booking.historyState = 0
    booking.save()
    responses["status"] = "Room Added Successfully"
    return success_response(responses)

# def isBookingAllowed():
#     fail = {}
#     responses = {}
#     data = json.loads(request.body.decode('utf-8'))
#     roomBookings = Bookings.objects.filter(roomId__exact=roomId).filter(endTime__lt=data.startTime).
#     if isUserAuthorized(userId):
#         for index in roomBookings:
#             if data.startTime < 


def isUserAuthorized(userId):
    user = User.objects.get(userId__exact=userId)
    history = Booking.object.filter(userId__exact=userId).values("historyStates")

    if user.role > 2:
        return false
    for index in history:
        if index == 1:
            return false  
    return true

@api_view(['GET'])
def getBookings():
     try:
        bookings = Booking.objects.all().values()
        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)