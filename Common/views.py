# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

import jwt
from django.http import JsonResponse
from django.shortcuts import render
import boto3
from boto3.s3.transfer import S3Transfer

from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Create your views here.
from django_base_template.settings import *


def invalid_method():
    failure_res = {'message': + ('Invalid method'), 'status': 'fail'}
    return JsonResponse(failure_res, status=405)


def failure_response(message):
    failure_res = {'content': message, 'status': 'Fail', 'error': 1}
    return JsonResponse(failure_res, status=501, safe=False, content_type="application/json")


def not_found_response(message):
    not_found_res = {'message': message, 'status': 'Not Found'}
    return JsonResponse(not_found_res, status=404, safe=False, content_type="application/json")


def success_response(success_res):
    response = {}
    response['status-code'] = 200
    response['error'] = 0
    response['sys_msg'] = ''
    response['message'] = 'Success!'
    response['content'] = success_res
    return JsonResponse(response, status=200, safe=False, content_type="application/json")


def login_failure_response(res):
    response = {}
    response['status-code'] = 401
    response['error'] = 1
    response['sys_msg'] = ''
    response['message'] = 'Login Failed'
    response['content'] = res
    return JsonResponse(response, status=401, safe=False, content_type="application/json")


def login_success_response(res):
    response = {}
    response['status-code'] = 200
    response['error'] = 0
    response['sys_msg'] = ''
    response['message'] = 'Login Success'
    response['content'] = res
    return JsonResponse(response, status=200, safe=False, content_type="application/json")


# Header Checker
def header_check(request):
    try:
        auth_header = request.META['HTTP_TOKEN']
        return True, auth_header
    except Exception as e:
        return False, "Null token not allowed"


# File upload with local storage
def file_upload_to_s3(filePath, file):
    try:
        transfer = S3Transfer(boto3.client('s3', AWS_REGION,
                                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY))
        bucket = AWS_STORAGE_BUCKET_NAME
        s3_path = 'media/temp/' + str(file)
        transfer.upload_file(str(filePath),
                             bucket,
                             s3_path,
                             extra_args={'ACL': 'public-read'})
        # Creating temporary directory in temp
        url = str(AWS_S3_CUSTOM_DOMAIN) + "/" + str(s3_path)
        return url
    except Exception as e:
        print(e)
        return 0


# File upload without local storage
def file_upload(file, fileName):
    try:
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
        k = Key(bucket)
        k.key = 'media/temp/' + str(fileName)
        k.set_contents_from_file(file)
        k.make_public()
        url = str(AWS_S3_CUSTOM_DOMAIN) + "/" + 'media/temp/' + str(fileName)
        return url
    except Exception as e:
        return 0


# For random digit
def random_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


# Extract Token
def token_extract(auth_header):
    res = jwt.decode(auth_header, SECRET_KEY)
    return res
