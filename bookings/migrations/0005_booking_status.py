from django.db import migrations, models


def populate_initial_status(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    Booking.objects.filter(status__isnull=True).update(status='ACTIVE')


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_globalsettings_system_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(
                choices=[('ACTIVE', 'Activa'), ('CANCELED', 'Cancelada'), ('COMPLETED', 'Completada')],
                default='ACTIVE',
                max_length=10,
            ),
        ),
        migrations.RunPython(populate_initial_status, migrations.RunPython.noop),
    ]
