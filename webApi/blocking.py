# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Blocking
from webApi.models import User
from webApi.services import sendMail


@api_view(['POST'])
def addBlock(request):
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

    blocking = Blocking()
    blocking.roomId = data['roomId']
    blocking.userId = data['userId']
    blocking.startTime = data['startTime']
    blocking.endTime = data['endTime']
    blocking.bookingDate = data['bookingDate']
    blocking.status = 1  # blocked
    booking.save()
    responses["status"] = "Room blocked Successfully"
    return success_response(responses)


# def updateBlockStatus(blockingId, newStatus):
#     Blocking.objects.filter(
#         blockingId__exact=blockingId).update(status=newStatus)
