"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import path,include

from visitors.views import (
    dashboard_view,
    TodaysVisitors
)
from visitors.views import CurrentVisitors
from visitors.views import CheckInVisitor
from visitors.views import CheckOutVisitor
from .admin import custom_admin_site
from visitors.models import Visitor, Department, Purpose


custom_admin_site.register(Visitor)
custom_admin_site.register(Department)
custom_admin_site.register(Purpose)



urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/visitors/',include ('visitors.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/todays-visitors/', TodaysVisitors.as_view(), name='todays_visitors'),
    path('api/current-visitors/', CurrentVisitors.as_view(), name='current_visitors'),
    path('api/checkin/', CheckInVisitor.as_view(), name='checkin'),
    path('api/checkout/<int:visitor_id>/', CheckOutVisitor.as_view(), name='checkout'),

]