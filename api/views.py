from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Visitors, AttendanceRecords, Users # Asume que Users es tu modelo para registered_by_user
from .serializers import VisitorSerializer, AttendanceRecordSerializer # Asegúrate de tener UserSerializer si lo necesitas
from django.utils import timezone
from django.db import transaction
from .serializers import VisitorSerializer, AttendanceRecordSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend



class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('id') # Es buena práctica ordenar
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser] # Ejemplo: Solo admins pueden gestionar usuarios

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitors.objects.all().order_by('id')
    serializer_class = VisitorSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['ci_number',]
    # permission_classes = [permissions.IsAuthenticated] # ¡Considera añadir permisos!

    @transaction.atomic # Asegura que ambas creaciones (Visitor y AttendanceRecord) ocurran o ninguna
    def create(self, request, *args, **kwargs):
        # 1. Crear el Visitante
        visitor_serializer = self.get_serializer(data=request.data)
        visitor_serializer.is_valid(raise_exception=True)
        # self.perform_create(visitor_serializer) # Esto guarda el visitante
        visitor_instance = visitor_serializer.save() # .save() también funciona y devuelve la instancia      
        attendance_data = {
            'visitor': visitor_instance.id,
            'entry_timestamp': timezone.now(), # Hora actual de entrada
            'visit_type': request.data.get('initial_visit_type', 'Registro Inicial'), # Valor por defecto o del request
            'notes': request.data.get('initial_notes', 'Creado automáticamente al registrar nuevo visitante.'), # Valor por defecto o del request
        }

        # Opcional: Asignar el usuario que registra, si hay autenticación
        if request.user.is_authenticated:
            try:
                user_instance = Users.objects.get(id=request.user.id) # O username=request.user.username
                attendance_data['registered_by_user'] = user_instance.id
            except Users.DoesNotExist:
                pass


        attendance_serializer = AttendanceRecordSerializer(data=attendance_data)
        
        if attendance_serializer.is_valid():
            attendance_serializer.save()
            
            headers = self.get_success_headers(visitor_serializer.data)
            response_data = {
                'visitor': visitor_serializer.data,
                'first_attendance_record': attendance_serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            transaction.set_rollback(True) # Asegura el rollback
            return Response({
                "detail": "Visitor data was valid, but creating initial attendance record failed.",
                "visitor_errors": visitor_serializer.errors, # Aunque ya debería haber pasado la validación
                "attendance_errors": attendance_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecords.objects.select_related('visitor', 'registered_by_user').all().order_by('-entry_timestamp')
    serializer_class = AttendanceRecordSerializer
    # permission_classes = [permissions.IsAuthenticated] # Asegura que el usuario esté logueado

    def perform_create(self, serializer):
        save_kwargs = {}
        # 1. Establecer entry_timestamp si no fue provisto por el cliente
        if not serializer.validated_data.get('entry_timestamp'):
            save_kwargs['entry_timestamp'] = timezone.now()
        user = self.request.user
        if user and user.is_authenticated:
            try:
                if hasattr(user, 'id') and 'registered_by_user' not in serializer.validated_data:
                     # Intenta obtener la instancia de tu modelo Users si registered_by_user lo requiere
                    user_instance_for_fk = Users.objects.get(id=user.id) # O username=user.username
                    save_kwargs['registered_by_user'] = user_instance_for_fk
            except Users.DoesNotExist:
                pass # Opcionalmente, puedes asignar None si el campo lo permite
            except AttributeError:
                # Si request.user no tiene 'id' o la estructura esperada
                pass
        serializer.save(**save_kwargs)