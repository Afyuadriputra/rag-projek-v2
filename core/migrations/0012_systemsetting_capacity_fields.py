# Generated manually for capacity control fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_systemsetting_maintenance_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemsetting",
            name="registration_limit_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="max_registered_users",
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="registration_limit_message",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="concurrent_login_limit_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="max_concurrent_logins",
            field=models.PositiveIntegerField(default=300),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="concurrent_limit_message",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="staff_bypass_concurrent_limit",
            field=models.BooleanField(default=True),
        ),
    ]
