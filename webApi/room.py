# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
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
def addRoom(request):
    success = {
        message:"Room Added Successfully"
    }
    fail = {}
    fail['status'] = 500
    print request.META
    return JsonResponse(success)
    data = json.loads(request.body.decode('utf-8'))

    if 'roomId' not in data:
        fail['msg'] = "Please provide room id"
        return login_failure_response(fail)
    elif 'roomName' not in data:
        fail['msg'] = "Please provide room name"
        return login_failure_response(fail)
    elif 'utilities' not in data:
        fail['msg'] = "Please provide room utilities"
        return login_failure_response(fail)
    elif 'size' not in data:
        fail['msg'] = "Please provide room size"
        return login_failure_response(fail)

    payload = {
        'roomId': data.roomId,
        'roomName': data.roomName,
        'utilities':data.utilities,
        'size':data.size
    }

    return login_success_response(success)


@api_view(['GET'])
def get_login_data(request, *args, **kwargs):
    success = {}
    success['status'] = 200
    success['msg'] = 'Token getting success'

    fail = {}
    fail['status'] = 500

    status, auth_header = header_check(request)

    if status != True:
        fail['msg'] = auth_header
        return failure_response(fail)
    try:
        res = token_extract(auth_header)
        return success_response(res)
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
