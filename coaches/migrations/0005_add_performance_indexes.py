"""
Performance migration: add DB indexes on CoachProfile filter fields.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coaches", "0004_coachprofile_represent_self"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coachprofile",
            name="is_active",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name="coachprofile",
            name="status",
            field=models.CharField(
                blank=True, max_length=10,
                choices=[("AMATEUR", "Amateur"), ("PRO", "Pro")],
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name="coachprofile",
            name="visibility_mode",
            field=models.CharField(
                max_length=15, default="ALL",
                choices=[("ALL", "Pour tout le monde"), ("ALL_EXCEPT", "Pour tout le monde sauf"), ("SOME", "Pour quelques clubs")],
                db_index=True,
            ),
        ),
    ]
