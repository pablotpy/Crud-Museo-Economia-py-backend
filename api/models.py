from django.db import models


class AttendanceRecords(models.Model):
    id = models.AutoField(primary_key=True) # O models.IntegerField(primary_key=True) si no es autoincremental
    visitor = models.ForeignKey('Visitors', models.DO_NOTHING, db_comment='ID del visitante (de la tabla visitors) que realiz¾ esta visita.')
    entry_timestamp = models.DateTimeField(db_comment='Fecha y hora exactas de la entrada del visitante.')
    exit_timestamp = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de salida del visitante (opcional).')
    visit_type = models.CharField(max_length=50, blank=True, null=True, db_comment='CategorÝa del tipo de visita (opcional).')
    notes = models.TextField(blank=True, null=True, db_comment='Notas adicionales sobre esta visita especÝfica (opcional).')
    registered_by_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True, db_comment='ID del usuario del sistema que registr¾ esta entrada (opcional).')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de creaci¾n del registro de asistencia.')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n del registro de asistencia.')

    class Meta:
        managed = False
        db_table = 'attendance_records'
        db_table_comment = 'Registra cada instancia de visita de un visitante al museo.'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Users(models.Model):
    id = models.AutoField(primary_key=True) # O models.IntegerField(primary_key=True) si no es autoincremental
    username = models.CharField(unique=True, max_length=50, db_comment='Nombre de usuario para iniciar sesion (*Ej:Admin).')
    full_name = models.CharField(max_length=150, blank=True, null=True, db_comment='Nombre completo del usuario.')
    email = models.CharField(unique=True, max_length=255, db_comment='Correo electronico del usuario (·Ej:Admin).')
    password_hash = models.CharField(max_length=255, db_comment='Hash de la contrase±a del usuario.')
    role = models.CharField(max_length=50, db_comment='Rol del usuario en el sistema (ej: admin, staff).')
    is_active = models.BooleanField(blank=True, null=True, db_comment='Indica si la cuenta del usuario esta activa.')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de creacion de la cuenta del usuario.')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n de la cuenta del usuario.')

    class Meta:
        managed = False
        db_table = 'users'
        db_table_comment = 'Almacena informacion de los usuarios del sistema (personal del museo).'


class Visitors(models.Model):
    id = models.AutoField(primary_key=True) # O models.IntegerField(primary_key=True) si no es autoincremental
    ci_number = models.CharField(unique=True, max_length=50, db_comment='N·mero de CÚdula de Identidad del visitante, debe ser ·nico.')
    first_name = models.CharField(max_length=100, db_comment='Nombre(s) del visitante.')
    last_name = models.CharField(max_length=100, db_comment='Apellido(s) del visitante.')
    notes = models.TextField(blank=True, null=True, db_comment='Notas adicionales sobre esta visita especÝfica (opcional).')
    visit_type = models.CharField(max_length=50, blank=True, null=True, db_comment='CategorÝa del tipo de visita (opcional).')
    country = models.CharField(max_length=100, blank=True, null=True, db_comment='PaÝs de origen del visitante.')
    email = models.CharField(unique=True, max_length=255, blank=True, null=True, db_comment='Correo electr¾nico del visitante (opcional, ·nico).')
    phone_number = models.CharField(max_length=50, blank=True, null=True, db_comment='N·mero de telÚfono del visitante (opcional).')
    date_of_birth = models.DateField(blank=True, null=True, db_comment='Fecha de nacimiento del visitante (opcional).')
    additional_data = models.JSONField(blank=True, null=True, db_comment='Campo JSON para datos adicionales obtenidos de fuentes externas (opcional).')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de creaci¾n del registro del visitante.')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n del registro del visitante.')

    class Meta:
        managed = False
        db_table = 'visitors'
        db_table_comment = 'Almacena informacion ·nica de cada visitante del museo.'
