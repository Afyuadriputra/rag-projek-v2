# Generated manually for user login presence tracking

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0012_systemsetting_capacity_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserLoginPresence",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=128, unique=True)),
                ("ip_address", models.CharField(blank=True, default="", max_length=64)),
                ("user_agent", models.CharField(blank=True, default="", max_length=512)),
                ("logged_in_at", models.DateTimeField(auto_now_add=True)),
                ("last_seen_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("logged_out_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="login_presences",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-last_seen_at"],
            },
        ),
        migrations.AddIndex(
            model_name="userloginpresence",
            index=models.Index(fields=["is_active", "last_seen_at"], name="core_userlo_is_acti_1f1838_idx"),
        ),
        migrations.AddIndex(
            model_name="userloginpresence",
            index=models.Index(fields=["user", "is_active"], name="core_userlo_user_id_6cad17_idx"),
        ),
    ]
