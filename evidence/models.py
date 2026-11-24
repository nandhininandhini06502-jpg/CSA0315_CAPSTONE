import os
import hashlib
from django.db import models
from django.conf import settings

def evidence_upload_path(instance, filename):
    return f"evidence/{filename}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-folder')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Evidence(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending Verification'),
        ('Verified', 'Verified (Integrity Confirmed)'),
        ('Rejected', 'Rejected / Invalid'),
    )

    evidence_id = models.AutoField(primary_key=True)
    evidence_code = models.CharField(max_length=20, unique=True, blank=True, help_text="e.g. E101")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evidences')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='evidences')
    file = models.FileField(upload_to=evidence_upload_path)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.BigIntegerField(default=0, help_text="Size in bytes")
    file_hash = models.CharField(max_length=64, blank=True, help_text="SHA-256 Digest")
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        # Generate evidence code if not present
        super_save = False
        if not self.pk:
            super().save(*args, **kwargs)
            super_save = True
            if not self.evidence_code:
                self.evidence_code = f"E{100 + self.evidence_id}"

        # If file is present, calculate sha256 hash
        if self.file and (not self.file_hash or 'file' in kwargs.get('update_fields', [])):
            try:
                self.file.seek(0)
                sha256 = hashlib.sha256()
                for chunk in self.file.chunks():
                    sha256.update(chunk)
                self.file_hash = sha256.hexdigest()
                self.file.seek(0)
                if hasattr(self.file, 'size'):
                    self.file_size = self.file.size
            except Exception:
                pass

        if not super_save:
            super().save(*args, **kwargs)
        else:
            super().save(update_fields=['evidence_code', 'file_hash', 'file_size'])

    @property
    def formatted_size(self):
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"

    @property
    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ""

    @property
    def is_image(self):
        return self.file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

    @property
    def is_video(self):
        return self.file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.webm']

    @property
    def is_audio(self):
        return self.file_extension in ['.mp3', '.wav', '.ogg', '.m4a', '.flac']

    @property
    def is_pdf(self):
        return self.file_extension == '.pdf'

    def __str__(self):
        return f"{self.evidence_code or ('E' + str(self.evidence_id))} - {self.title}"


class Verification(models.Model):
    STATUS_CHOICES = (
        ('Verified', 'Verified (Integrity Confirmed)'),
        ('Tampered', 'Tampered / Hash Mismatch'),
        ('Rejected', 'Rejected by Administrator'),
    )

    verification_id = models.AutoField(primary_key=True)
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name='verifications')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='performed_verifications')
    original_hash = models.CharField(max_length=64)
    current_hash = models.CharField(max_length=64)
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    verification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification #{self.verification_id} - {self.evidence.evidence_code}: {self.verification_status}"


class AuditLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=100)
    evidence = models.ForeignKey(Evidence, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.action} by {self.user.username if self.user else 'System'}"


class EvidenceAccess(models.Model):
    access_id = models.AutoField(primary_key=True)
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name='access_records')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evidence_accesses')
    action = models.CharField(max_length=50, default='VIEW')  # VIEW, DOWNLOAD, VERIFY
    access_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-access_date']

    def __str__(self):
        return f"{self.user.username} {self.action} {self.evidence.evidence_code} at {self.access_date}"
