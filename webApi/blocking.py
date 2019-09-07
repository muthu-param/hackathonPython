# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Blocking
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
def addBlock(roomId,userId,startTime,endTime,bookingDate):
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

    blocking = Blocking()
    blocking.roomId = data['roomId']
    blocking.userId = data['userId']
    blocking.startTime = data['startTime']
    blocking.endTime = data['endTime']
    blocking.bookingDate = data['bookingDate']
    blocking.status = 1 ##blocked
    booking.save()
    responses["status"] = "Room Added Successfully"
    return success_response(responses)

def updateBlockStatus(blockingId,newStatus):
    Blocking.objects.filter(blockingId__exact=blockingId).update(status=newStatus)