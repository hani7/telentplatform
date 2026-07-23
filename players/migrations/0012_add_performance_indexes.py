"""
Performance migration: add DB indexes on the most-queried filter fields.

Fields indexed:
  PlayerProfile : is_active, status, position, foot, visibility_mode, height_cm, desired_salary
  CoachProfile  : is_active, status, visibility_mode
  Offer         : sender, recipient, status

These fields are used in WHERE clauses on every dashboard / search page load.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0011_playerprofile_parent_address_and_more"),
    ]

    operations = [
        # ── PlayerProfile indexes ─────────────────────────────────────────────
        migrations.AlterField(
            model_name="playerprofile",
            name="is_active",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name="playerprofile",
            name="status",
            field=models.CharField(
                blank=True, max_length=10,
                choices=[("AMATEUR", "Amateur"), ("PRO", "Pro")],
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name="playerprofile",
            name="position",
            field=models.CharField(max_length=50, blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="playerprofile",
            name="foot",
            field=models.CharField(
                max_length=1, blank=True,
                choices=[("R", "Droit"), ("L", "Gauche"), ("B", "Les 2")],
                db_index=True,
            ),
        ),
        migrations.AlterField(
            model_name="playerprofile",
            name="visibility_mode",
            field=models.CharField(
                max_length=15, default="ALL",
                choices=[("ALL", "Pour tout le monde"), ("ALL_EXCEPT", "Pour tout le monde sauf"), ("SOME", "Pour quelques clubs")],
                db_index=True,
            ),
        ),
    ]
