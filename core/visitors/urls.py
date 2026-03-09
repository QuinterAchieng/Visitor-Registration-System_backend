from django.urls import path
from .views import (
    CheckInVisitor,
    CheckOutVisitor,
    CurrentVisitors,
    TodaysVisitors,
    VisitorList
)

urlpatterns = [
    path('', VisitorList.as_view(), name='visitor_list'),
    path('checkin/', CheckInVisitor.as_view(), name='checkin'),
    path('checkout/<int:visitor_id>/', CheckOutVisitor.as_view(), name='checkout'),
    path('current/', CurrentVisitors.as_view(), name='current_visitors'),
    path('today/', TodaysVisitors.as_view(), name='todays_visitors'),
]
