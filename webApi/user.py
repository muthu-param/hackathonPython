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
def login(request):
    success = {}
    fail = {}
    fail['status'] = 500
    print request.META
    return JsonResponse(success)
    data = json.loads(request.body.decode('utf-8'))

    if 'user_name' not in data:
        fail['msg'] = "Please provide User Name"
        return login_failure_response(fail)
    elif 'password' not in data:
        fail['msg'] = "Please provide Password"
        return login_failure_response(fail)

    try:
        user = User.objects.get(user_name=data['user_name'], password=data['password'])
    except User.DoesNotExist:
        fail['msg'] = "Invalid username/password"
        return login_failure_response(fail)

    if user:
        payload = {
            'id': user.user_id,
            'email': user.email,
        }

        success['token'] = jwt.encode(payload, SECRET_KEY)
        # Send mail to user
        sendMail(user.user_name, user.email)

        return login_success_response(success)
    else:
        fail['msg'] = "Invalid credentials"
        return login_failure_response(fail)


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
