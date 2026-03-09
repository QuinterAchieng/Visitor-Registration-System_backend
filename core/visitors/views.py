from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from .models import AuditLog
from .audit import log_action
from .serializers import AuditLogSerializer

class AuditLogListView(ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]

from .models import Visitor
from .serializers import VisitorSerializer
from .permissions import IsDeskOfficer


class CheckInVisitor(APIView):
    permission_classes = [IsAuthenticated, IsDeskOfficer]

    def post(self, request):
        print("LOGGED USER:", request.user.username)

        serializer = VisitorSerializer(data=request.data)

        if serializer.is_valid():
            visitor = serializer.save(
                recorded_by=request.user,
                check_in_time=timezone.now(),
                checked_out=False
            )

            #  CREATE AUDIT LOG
            AuditLog.objects.create(
                user=request.user,
                action='CREATE',
                visitor=visitor,
                description=f"{request.user.username} checked in visitor {visitor.full_name}"
            )

            log_action(
                user=request.user,
                visitor=visitor,
                action="CREATE",
                description=f"{request.user.username} checked in {visitor.full_name}"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitorList(APIView):
    permission_classes = [IsAuthenticated, IsDeskOfficer]

    def get(self, request):
        visitors = Visitor.objects.all().order_by('-check_in_time')
        serializer = VisitorSerializer(visitors, many=True)
        return Response(serializer.data)


class CurrentVisitors(APIView):
    permission_classes = [IsAuthenticated, IsDeskOfficer]

    def get(self, request):
        visitors = Visitor.objects.filter(checked_out=False)
        serializer = VisitorSerializer(visitors, many=True)
        return Response(serializer.data)

from datetime import date
from .serializers import VisitorSerializer


class TodaysVisitors(APIView):
    permission_classes = [IsAuthenticated, IsDeskOfficer]

    def get(self, request):
        today = date.today()
        visitors = Visitor.objects.filter(check_in_time__date=today)
        serializer = VisitorSerializer(visitors, many=True)
        return Response(serializer.data)


class CheckOutVisitor(APIView):
    permission_classes = [IsAuthenticated, IsDeskOfficer]

    def post(self, request, visitor_id):
        try:
            visitor = Visitor.objects.get(id=visitor_id)
        except Visitor.DoesNotExist:
            return Response(
                {"error": "Visitor not found"},
                status=status.HTTP_404_NOT_FOUND
            )

          # Checkout logic
        visitor.checked_out = True
        visitor.check_out_time = timezone.now()
        visitor.checked_out_by = request.user
        visitor.save()

        # Audit log
        AuditLog.objects.create(
            user=request.user,
            action="CHECKOUT",
            visitor=visitor,
            description=f"{request.user.username} checked out {visitor.full_name}"
        )

        return Response(
            {"success": "Visitor checked out"},
            status=status.HTTP_200_OK
        )
from django.shortcuts import render
from datetime import date


from django.utils import timezone
from .models import Visitor

def dashboard_view(request):

    today = timezone.now().date()

    total_visitors = Visitor.objects.count()

    current_visitors = Visitor.objects.filter(
        checked_out=False
    ).count()

    today_checkins = Visitor.objects.filter(
        check_in_time__date=today
    ).count()

    today_checkouts = Visitor.objects.filter(
        check_out_time__date=today
    ).count()

    departments_visited = Visitor.objects.filter(
        check_in_time__date=today
    ).values('department').distinct().count()

    context = {
        "total_visitors": total_visitors,
        "current_visitors": current_visitors,
        "today_checkins": today_checkins,
        "today_checkouts": today_checkouts,
        "departments_visited": departments_visited
    }

    return render(request, "admin/dashboard.html", context)