from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollrun',
            name='month',
            field=models.DateField(
                help_text='The month and year for this payroll run (use the first day of month)',
                unique=True,
            ),
        ),
    ]
