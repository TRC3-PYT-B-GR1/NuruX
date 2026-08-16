from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appversion',
            name='apk_file',
            field=models.FileField(
                blank=True,
                help_text='Optional local APK upload. Use download_url for ephemeral hosting platforms.',
                null=True,
                upload_to='apks/',
            ),
        ),
        migrations.AddField(
            model_name='appversion',
            name='download_url',
            field=models.URLField(
                blank=True,
                help_text='Durable external URL, such as a GitHub Release asset.',
            ),
        ),
    ]
