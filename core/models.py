from django.db import models
from django.contrib.auth.models import User
import os

class AcademicDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    # File akan disimpan di media/documents/tahun/bulan/
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_embedded = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        # Auto-fill title dari nama file jika kosong
        if not self.title:
            self.title = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Chat Baru")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, null=True, blank=True, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # Yang terbaru muncul duluan

    def __str__(self):
        return f"{self.user.username}: {self.question[:20]}..."


class UserQuota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quota_bytes = models.BigIntegerField(default=10 * 1024 * 1024)  # default 10MB
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} quota={self.quota_bytes}B"


class LLMConfiguration(models.Model):
    """
    Konfigurasi runtime LLM berbasis DB.
    Bisa CRUD via Django Admin, dan sistem memakai konfigurasi yang aktif terbaru.
    """
    name = models.CharField(max_length=100, default="Default")
    is_active = models.BooleanField(default=True)
    openrouter_api_key = models.CharField(max_length=255, blank=True)
    openrouter_model = models.CharField(
        max_length=255,
        default="qwen/qwen3-next-80b-a3b-instruct:free",
    )
    openrouter_backup_models = models.TextField(
        blank=True,
        default="",
        help_text="Daftar model backup, pisahkan dengan baris baru atau koma.",
    )
    openrouter_timeout = models.PositiveIntegerField(default=45)
    openrouter_max_retries = models.PositiveIntegerField(default=1)
    openrouter_temperature = models.FloatField(default=0.2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.name} ({status})"


class SystemSetting(models.Model):
    """
    Singleton pengaturan sistem global.
    """
    registration_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SystemSetting(registration_enabled={self.registration_enabled})"
