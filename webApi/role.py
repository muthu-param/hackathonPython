# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, jwt
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from Common.views import *
from django_base_template.settings import SECRET_KEY
from webApi.models import User, Role
from webApi.services import sendMail


@api_view(['GET'])
def getRole(request, *args, **kwargs):
    success = {}
    success['status'] = 200
    success['msg'] = 'Token getting success'

    fail = {}
    fail['status'] = 500

    # status, auth_header = header_check(request)

    # if status != True:
    #     fail['msg'] = auth_header
    #     return failure_response(fail)

    try:
        roles = Role.objects.all().values()
        return success_response(list(roles))
    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)
