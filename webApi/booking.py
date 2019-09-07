# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Booking, Room, User, MoM
from webApi.models import User
from webApi.services import sendMail


@api_view(['POST'])
def addBooking(request):
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
    elif 'endTime' not in data:
        fail['msg'] = "Please provide end time"
        return failure_response(fail)
    elif 'bookingDate' not in data:
        fail['msg'] = "Please provide booking date"
        return failure_response(fail)
    elif 'agenda' not in data:
        fail['msg'] = "Please provide agenda"
        return failure_response(fail)

    booking = Booking()
    booking.roomId = Room.objects.get(roomId=data['roomId'])
    booking.userId = User.objects.get(userId=data['userId'])
    booking.startTime = data['startTime']
    booking.endTime = data['endTime']
    booking.agenda = data['agenda']
    booking.historyState = 0
    booking.save()
    responses["status"] = "Room Added Successfully"
    return success_response(responses)


@api_view(['GET'])
def userAuthorizedForBooking(request):
    responses = {
        "msg": "!Success"
    }
    fail = {}
    userId = request.GET['userId']
    user = User.objects.get(userId=userId)

    history = Booking.objects.filter(
        userId=userId).values('historyState')

    if user.role > 2:
        fail['msg'] = "Can't book the room"
        return failure_response(fail)

    for index in history:
        if index["historyState"] == 1:
            fail['msg'] = "Please provide MoM for previous booking"
            return failure_response(fail)
    return success_response(responses)


@api_view(['GET'])
def getBookings(request, *args, **kwargs):
    fail = {}
    try:
        bookings = Booking.objects.all().values()
        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)


@api_view(['GET'])
def getBookingsById(request):
    fail = {}
    try:
        userId = request.GET['userId']
        # bookings = Booking.objects.filter(userId_id=userId)
        # return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)

@api_view(['GET'])
def getBookingsByDate(date):
     try:
        bookings = Booking.objects.filter(startTime__date=datetime.date(date))
        data={}
        for i in bookings:
            data[i["roomId"]] = []
        for i in bookings:
            data[i["roomId"]].append({"roomName": i["roomName"], "bookingId": i["bookingId]", "startTime": i["startTime"], "endTime": i["endTime"], "bookingDate": i["bookingDate"] })

        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)

@api_view(['POST'])
def addMoM(request):
    fail = {}
    responses = {}
    data = json.loads(request.body.decode('utf-8'))

    if 'bookingId' not in data:
        fail['msg'] = "Please provide booking Id"
        return failure_response(fail)
    elif 'userId' not in data:
        fail['msg'] = "Please provide user id"
        return failure_response(fail)
    elif 'roomId' not in data:
        fail['msg'] = "Please provide room Id"
        return failure_response(fail)
    elif 'aboutMoM' not in data:
        fail['msg'] = "Please provide aboutMoM"
        return failure_response(fail)
    elif 'remarks' not in data:
        fail['msg'] = "Please provide remarks"
        return failure_response(fail)
    elif 'projectTitle' not in data:
        fail['msg'] = "Please provide projectTitle"
        return failure_response(fail)

    mom = MoM()
    mom.bookingId = Booking.objects.get(bookingId=data['bookingId'])
    mom.userId = User.objects.get(userId=data['userId'])
    mom.roomId = Room.objects.get(roomId=data['roomId'])
    mom.aboutMoM = data['aboutMoM']
    mom.remarks = data['remarks']
    mom.projectTitle = data['projectTitle']
    mom.save()
    responses["status"] = "Room MoM Successfully"
    return success_response(responses)
