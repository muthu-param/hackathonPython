from django.conf.urls import url
from webApi import views, services, role, user, room, booking

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

    url(r'^getUsers', user.getUsers, name='getUsers'),

    url(r'^addRoom', room.addRoom, name='addRoom'),

    url(r'^updateRoom', room.updateRoom, name='updateRoom'),    

    url(r'^getRooms', room.getRooms, name='getRooms'),

    url(r'^addMoM', booking.addMoM, name='addMoM'),    

    url(r'^bookRoom', booking.addBooking, name='bookRoom'),

    url(r'^userAuthorizedForBooking/$', booking.userAuthorizedForBooking, name='userAuthorizedForBooking'),

    url(r'^getBookings', booking.getBookings, name='getBookings'),

    url(r'^allBookingById', booking.getBookingsById, name='getBookingsById'),

    url(r'^ByDate', booking.getBookingsByDate, name='getBookingsByDate'),

]
