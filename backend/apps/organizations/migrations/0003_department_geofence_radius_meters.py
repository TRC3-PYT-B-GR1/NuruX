from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0002_department_description_department_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='geofence_radius_meters',
            field=models.PositiveIntegerField(
                default=200,
                help_text='Maximum distance from the department location for attendance scans.',
            ),
        ),
    ]
