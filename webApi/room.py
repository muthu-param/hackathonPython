# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import jwt
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
    fail = {}
    responses = {}
    data = json.loads(request.body.decode('utf-8'))

    if 'roomName' not in data:
        fail['msg'] = "Please provide room name"
        return failure_response(fail)
    elif 'size' not in data:
        fail['msg'] = "Please provide room size"
        return failure_response(fail)

    room = Room()
    room.roomName = data['roomName']
    room.size = data['size']
    room.utilityAC = data['utilityAC']
    room.utilitySmTv = data['utilitySmTv']
    room.utilityWater = data['utilityWater']
    room.utilityWBoard = data['utilityWBoard']
    room.utilityProjector = data['utilityProjector']
    room.createdBy = data['createdBy']
    room.status = 'Active'
    room.save()
    responses["status"] = "Room Added Successfully"
    return success_response(responses)


@api_view(['POST'])
def updateRoom(request):
    fail = {}
    responses = {
        "msg": "!Successfully updated"
    }
    data = json.loads(request.body.decode('utf-8'))
    if 'roomId' not in data:
        fail['msg'] = "Please provide room Id"
        return failure_response(fail)
    elif 'roomName' not in data:
        fail['msg'] = "Please provide room name"
        return failure_response(fail)
    elif 'size' not in data:
        fail['msg'] = "Please provide room size"
        return failure_response(fail)

    room = Room.objects.filter(roomId=data['roomId']).update(
        roomName=data['roomName'], size=data['size'], utilityAC=data['utilityAC'], utilitySmTv=data['utilitySmTv'], utilityWater=data['utilityWater'], utilityWBoard=data['utilityWBoard'], utilityProjector=data['utilityProjector'])

    return success_response(responses)


@api_view(['GET'])
def getRooms(request, *args, **kwargs):
    fail = {}
    try:
        rooms = Room.objects.all().values()
        return success_response(list(rooms))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
