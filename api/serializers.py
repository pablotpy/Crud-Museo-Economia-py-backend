from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework import serializers
from .models import Visitors, AttendanceRecords, Users


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


#---------------------------------------------------------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' # Incluye todos los campos
        # Considera excluir 'password_hash' en respuestas GET o hacerlo write_only
        # extra_kwargs = {
        #     'password_hash': {'write_only': True, 'required': False}
        # }

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitors
        fields = '__all__'
        # Ejemplo de campos específicos si no quieres todos:
        # fields = ['id', 'ci_number', 'first_name', 'last_name', 'country', 'email', 'phone_number', 'date_of_birth', 'created_at', 'updated_at']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    visitor_ci = serializers.CharField(source='visitor.ci_number', read_only=True, allow_null=True)
    visitor_name = serializers.SerializerMethodField(read_only=True)
    user_username = serializers.CharField(source='registered_by_user.username', read_only=True, allow_null=True)

    # Para escritura, aceptamos el ID.
    visitor = serializers.PrimaryKeyRelatedField(queryset=Visitors.objects.all())
    registered_by_user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), allow_null=True, required=False)

    class Meta:
        model = AttendanceRecords
        fields = [
            'id', 
            'visitor', 
            'visitor_ci', 
            'visitor_name', 
            'entry_timestamp', 
            'exit_timestamp', 
            'visit_type', 
            'notes', 
            'registered_by_user', 
            'user_username',
            'created_at', 
            'updated_at'
        ]
        extra_kwargs = {
            'entry_timestamp': {'required': False, 'allow_null': True}, # Backend puede ponerlo si es null
            'exit_timestamp': {'required': False, 'allow_null': True},
            'visit_type': {'required': False, 'allow_blank': True, 'allow_null': True},
            'notes': {'required': False, 'allow_blank': True, 'allow_null': True},
        }
        read_only_fields = ('created_at', 'updated_at', 'visitor_ci', 'visitor_name', 'user_username')

    def get_visitor_name(self, obj):
        if obj.visitor:
            return f"{obj.visitor.first_name} {obj.visitor.last_name}"
        return None

