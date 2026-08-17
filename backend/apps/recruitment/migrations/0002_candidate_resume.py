import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("recruitment", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="candidate",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="recruitment/resumes/",
                validators=[django.core.validators.FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
            ),
        ),
    ]
