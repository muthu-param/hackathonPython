from django.conf.urls import url
from webApi import views, services, role, user

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # login
    url(r'^login$', views.login, name='login'),

    # sample API with Auth
    url(r'^check', views.get_login_data, name='get login data'),

    # File upload
    url(r'^imageUpload', services.image_upload, name='File Upload'),

    # Send mail
    url(r'^sendMail', services.sendMail, name='Mail send'),

    url(r'^getRole', role.getRole, name='getRole'),

    url(r'^addUser', user.addUser, name='addUser'),

]
