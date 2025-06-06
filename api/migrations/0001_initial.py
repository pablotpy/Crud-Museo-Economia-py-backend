# Generated by Django 5.2.1 on 2025-05-19 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('entry_timestamp', models.DateTimeField(db_comment='Fecha y hora exactas de la entrada del visitante.')),
                ('exit_timestamp', models.DateTimeField(blank=True, db_comment='Fecha y hora de salida del visitante (opcional).', null=True)),
                ('visit_type', models.CharField(blank=True, db_comment='CategorÝa del tipo de visita (opcional).', max_length=50, null=True)),
                ('notes', models.TextField(blank=True, db_comment='Notas adicionales sobre esta visita especÝfica (opcional).', null=True)),
                ('created_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de creaci¾n del registro de asistencia.', null=True)),
                ('updated_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n del registro de asistencia.', null=True)),
            ],
            options={
                'db_table': 'attendance_records',
                'db_table_comment': 'Registra cada instancia de visita de un visitante al museo.',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_comment='Nombre de usuario para iniciar sesi¾n (·nico).', max_length=50, unique=True)),
                ('full_name', models.CharField(blank=True, db_comment='Nombre completo del usuario.', max_length=150, null=True)),
                ('email', models.CharField(db_comment='Correo electr¾nico del usuario (·nico).', max_length=255, unique=True)),
                ('password_hash', models.CharField(db_comment='Hash de la contrase±a del usuario.', max_length=255)),
                ('role', models.CharField(db_comment='Rol del usuario en el sistema (ej: admin, staff).', max_length=50)),
                ('is_active', models.BooleanField(blank=True, db_comment='Indica si la cuenta del usuario estß activa.', null=True)),
                ('created_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de creaci¾n de la cuenta del usuario.', null=True)),
                ('updated_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n de la cuenta del usuario.', null=True)),
            ],
            options={
                'db_table': 'users',
                'db_table_comment': 'Almacena informacion de los usuarios del sistema (personal del museo).',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ci_number', models.CharField(db_comment='N·mero de CÚdula de Identidad del visitante, debe ser ·nico.', max_length=50, unique=True)),
                ('first_name', models.CharField(db_comment='Nombre(s) del visitante.', max_length=100)),
                ('last_name', models.CharField(db_comment='Apellido(s) del visitante.', max_length=100)),
                ('country', models.CharField(blank=True, db_comment='PaÝs de origen del visitante.', max_length=100, null=True)),
                ('email', models.CharField(blank=True, db_comment='Correo electr¾nico del visitante (opcional, ·nico).', max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, db_comment='N·mero de telÚfono del visitante (opcional).', max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, db_comment='Fecha de nacimiento del visitante (opcional).', null=True)),
                ('additional_data', models.JSONField(blank=True, db_comment='Campo JSON para datos adicionales obtenidos de fuentes externas (opcional).', null=True)),
                ('created_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de creaci¾n del registro del visitante.', null=True)),
                ('updated_at', models.DateTimeField(blank=True, db_comment='Fecha y hora de la ·ltima actualizaci¾n del registro del visitante.', null=True)),
            ],
            options={
                'db_table': 'visitors',
                'db_table_comment': 'Almacena informacion ·nica de cada visitante del museo.',
                'managed': False,
            },
        ),
    ]
