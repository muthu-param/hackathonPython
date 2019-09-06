import json

from django.utils.deprecation import MiddlewareMixin

from django_base_template.settings import logger


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Request Middleware")
        breaks = "\n----------------------"
        ip = "\n\nIP : [ " + request.META.get('REMOTE_ADDR') + " ]"
        method = " Method : [ " + request.method + " ]"
        path = " Path : [ " + request.path + " ]"
        meta_data = " Meta : [ " + str(request.META) + " ]"
        # UserAgent = " User Agent : [ " + request.META.get('HTTP_USER_AGENT') + " ]"
        # Accept = " Accept : [ " + request.META.get('HTTP_ACCEPT') + " ]"
        # HTTPACCEPTENCODING = " HTTP ACCEPT ENCODING : [ " + request.META.get('HTTP_ACCEPT_ENCODING') + " ]"
        if not request.FILES:
            data = " data : [ " + json.dumps(request.body.decode('utf-8')) + " ]"
        else:
            data = request.FILES
        try:
            logger.debug(breaks + ip + method + path + str(meta_data) + data)
        except Exception as e:
            logger.debug(e.message)
        return None


class ResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print("Response Middleware")
        breaks = "\n\n----------------------\n\n"
        logger.debug("\n\n" + str(response) + breaks)
        return response
