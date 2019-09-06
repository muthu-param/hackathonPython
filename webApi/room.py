# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import Room
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
def addRoom(request):
    print request.META
    return JsonResponse(success)
    data = json.loads(request.body.decode('utf-8'))

    if 'roomId' not in data:
        fail['msg'] = "Please provide room id"
        return failure_response(fail)
    elif 'roomName' not in data:
        fail['msg'] = "Please provide room name"
        return failure_response(fail)
    elif 'utilities' not in data:
        fail['msg'] = "Please provide room utilities"
        return failure_response(fail)
    elif 'size' not in data:
        fail['msg'] = "Please provide room size"
        return failure_response(fail)

    payload = {
        'roomId': data.roomId,
        'roomName': data.roomName,
        'utilities':data.utilities,
        'size':data.size
    }

    return success_response(success)


@api_view(['GET'])
def getRooms(request, *args, **kwargs):

    try:
        rooms = Room.objects.all().values()
        return success_response(list(rooms))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)