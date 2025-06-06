from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from .models import Visitors, AttendanceRecords, Users
from .serializers import VisitorSerializer, AttendanceRecordSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar los usuarios del sistema.
    """
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser] # Descomentar para activar permisos de admin


class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los visitantes.
    Permite buscar por número de CI.
    """
    queryset = Visitors.objects.all().order_by('id')
    serializer_class = VisitorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ci_number']
    # permission_classes = [permissions.IsAuthenticated] # Descomentar para activar permisos

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo Visitante y su primer Registro de Asistencia.
        Maneja inteligentemente el campo de notas.
        """
        # --- PASO DE DEPURACIÓN ---
        # Imprime los datos que llegan del frontend en tu terminal de Django.
        print("Datos recibidos en el backend:", request.data)
        # -------------------------

        visitor_serializer = self.get_serializer(data=request.data)
        visitor_serializer.is_valid(raise_exception=True)
        visitor_instance = visitor_serializer.save()

        # Lógica robusta para las notas
        notes_from_request = request.data.get('notes')
        default_notes = 'Creado automáticamente al registrar nuevo visitante.'
        
        # Se usa .strip() para eliminar espacios en blanco al inicio y al final.
        # Si después de eso la nota tiene texto, se usa; si no, se usa el valor por defecto.
        final_notes = notes_from_request if notes_from_request and notes_from_request.strip() else default_notes
        
        attendance_data = {
            'visitor': visitor_instance.id,
            'entry_timestamp': timezone.now(),
            'visit_type': request.data.get('visit_type', 'Registro Inicial'),
            'notes': final_notes,
        }

        user = request.user
        if user.is_authenticated:
            try:
                user_instance = Users.objects.get(id=user.id)
                attendance_data['registered_by_user'] = user_instance.id
            except Users.DoesNotExist:
                pass

        attendance_serializer = AttendanceRecordSerializer(data=attendance_data)
        if attendance_serializer.is_valid(raise_exception=True):
            attendance_serializer.save()
            headers = self.get_success_headers(visitor_serializer.data)
            response_data = {
                'visitor': visitor_serializer.data,
                'first_attendance_record': attendance_serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        
        # Este bloque es una salvaguarda, pero con raise_exception=True, un error de validación
        # ya habría lanzado una excepción.
        transaction.set_rollback(True)
        return Response({
            "detail": "Falló la creación del registro de asistencia inicial.",
            "attendance_errors": attendance_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los registros de asistencia de visitantes existentes.
    """
    queryset = AttendanceRecords.objects.select_related('visitor', 'registered_by_user').all().order_by('-entry_timestamp')
    serializer_class = AttendanceRecordSerializer
    # permission_classes = [permissions.IsAuthenticated] # Descomentar para activar permisos

    def perform_create(self, serializer):
        """
        Establece valores por defecto al crear un nuevo registro de asistencia.
        """
        save_kwargs = {}
        if not serializer.validated_data.get('entry_timestamp'):
            save_kwargs['entry_timestamp'] = timezone.now()
        
        user = self.request.user
        if user and user.is_authenticated:
            if hasattr(user, 'id') and 'registered_by_user' not in serializer.validated_data:
                try:
                    user_instance_for_fk = Users.objects.get(id=user.id)
                    save_kwargs['registered_by_user'] = user_instance_for_fk
                except Users.DoesNotExist:
                    pass
                except AttributeError:
                    pass
        
        serializer.save(**save_kwargs)