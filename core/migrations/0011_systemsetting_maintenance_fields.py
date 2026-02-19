from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_rename_core_planne_user_id_6eba0f_idx_core_planne_user_id_bd7ce9_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="systemsetting",
            name="allow_staff_bypass",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="maintenance_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="maintenance_estimated_end_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="maintenance_message",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="systemsetting",
            name="maintenance_start_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
