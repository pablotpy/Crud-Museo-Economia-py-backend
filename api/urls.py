from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VisitorViewSet, AttendanceRecordViewSet

# DefaultRouter crea automáticamente las URLs para las acciones CRUD estándar.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'visitors', VisitorViewSet, basename='visitor')
router.register(r'attendancerecords', AttendanceRecordViewSet, basename='attendancerecord')

urlpatterns = [
    path('', include(router.urls)),
]