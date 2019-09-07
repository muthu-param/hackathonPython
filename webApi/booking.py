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
from webApi.services import sendMail, sendMailToAll
from datetime import datetime, timedelta
from django.db.models import Q
import re
from textblob import TextBlob


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

    # Mail
    mailId = User.objects.filter(~Q(role=3)).values('email')
    mailIds = []
    for i in mailId:
        mailIds.append(i["email"])

    roomData = Room.objects.get(roomId=data['roomId'])
    userData = User.objects.get(userId=data['userId'])

    sendMailToAll(roomData.roomName, userData.userName,
                  mailIds, booking.startTime, booking.endTime)

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
        print userId
        bookings = Booking.objects.filter(userId_id=userId).values()
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

    momData = MoM.objects.filter(bookingId=data['bookingId']).values()
    print momData
    if len(momData) == 0:

        mom = MoM()
        mom.bookingId = Booking.objects.get(bookingId=data['bookingId'])
        mom.userId = User.objects.get(userId=data['userId'])
        mom.roomId = Room.objects.get(roomId=data['roomId'])
        mom.aboutMoM = data['aboutMoM']
        mom.remarks = data['remarks']
        mom.projectTitle = data['projectTitle']
        sentiment, polarity = get_tweet_sentiment(data['aboutMoM'])
        print polarity
        mom.sentiment = sentiment
        mom.polarity = polarity * 100
        mom.save()

        Booking.objects.filter(
            bookingId=data['bookingId']).update(historyState=2)
        responses["status"] = "Room MoM Successfully"
        return success_response(responses)
    else:
        fail = {
            "error": "Already Existing"
        }
        return success_response(fail)


@api_view(['POST'])
def getBookingsByDate(request):
    data = json.loads(request.body.decode('utf-8'))
    fail = {}
    try:

        from_date = datetime.strptime(data['date'], '%Y-%m-%d')
        to_date = datetime.strptime(data['date'], '%Y-%m-%d')
        last_time = to_date.replace(hour=23, minute=59, second=59)

        bookings = Booking.objects.filter(
            startTime__range=[from_date, last_time]).values()
        return success_response(list(bookings))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)


def clean_tweet(tweet):
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(msg):
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(msg))
    # set sentiment
    polarity = analysis.sentiment.polarity
    print polarity
    if polarity > 0:
        return ('positive', polarity)
    elif polarity == 0:
        return ('neutral', polarity)
    else:
        return ('negative', polarity)


@api_view(['GET'])
def getMoM(request):
    fail = {}
    try:
        momId = request.GET['bookingId']
        momData = MoM.objects.filter(bookingId=momId).values()
        return success_response(list(momData))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
