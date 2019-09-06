# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import User
from webApi.services import sendMail


@api_view(['POST'])
def addUser(request):
    responses = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        user = User()
        user.userId = data['userId']
        user.userName = data['userName']
        user.password = data['password']
        user.email = data['email']
        user.createdBy = data['createdBy']
        user.role = data['role']
        user.status = 'Active'
        user.save()
        responses["status"] = "User Added Successfully"
        sendMail(user.userName, user.email)
        return success_response(responses)
    except Exception as err:
        return failure_response(err.message)


@api_view(['GET'])
def getUsers(request, *args, **kwargs):
    fail = {}
    try:
        users = User.objects.all().values(
            'userName', 'userId', 'role', 'createdBy', 'email')
        return success_response(list(users))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
