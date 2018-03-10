from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^inbound/sms/$', api.InboundSMS.as_view()),
    url(r'^outbound/sms/$', api.OutboundSMS.as_view())
]
