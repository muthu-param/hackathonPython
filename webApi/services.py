import base64
import json
import tempfile

from django.core.mail import send_mail

from rest_framework.decorators import api_view

from Common.views import *
from django.template.loader import render_to_string


@api_view(['POST'])
def image_upload(request):
    fail = {}
    try:
        file = request.FILES['file']
        name = file.name
        extension = name.split(".")[-1]
        if not file:
            fail['msg'] = str('Key Mismatch')
            return failure_response(fail)
        else:
            url = file_upload(file, str(random_digits(5)) + extension)

            # if using base64 image format

            # if 'file' in rawData.keys():
            # with tempfile.NamedTemporaryFile(delete=True) as imgFile:
            #     # imgFile.write(base64.b64decode(rawData['file'].split(',')[1]))
            #     imgFile.write(file.name)
            #     imgFile.truncate()
            #     url = file_upload_to_s3(imgFile.name, str(random_digits(5)) + ".png")

            res = {}
            res['image_url'] = url
            return success_response(res)

    except Exception as e:
        fail['msg'] = str(e)
        return failure_response(fail)


def sendMail(username, email):
    try:
        subject = "Django Testing"
        ctx = {
            'username': username
        }

        message = render_to_string('django_email_template.html', ctx)

        send_mail(subject, message, 'divumtab@gmail.com', [email],
                  fail_silently=False)
        return 1
    except Exception as e:
        return 0
