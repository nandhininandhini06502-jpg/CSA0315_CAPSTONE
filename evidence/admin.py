from django.contrib import admin
from .models import Category, Evidence, Verification, AuditLog, EvidenceAccess

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'icon', 'created_at')
    search_fields = ('category_name', 'description')


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('evidence_code', 'title', 'category', 'user', 'file_type', 'formatted_size', 'status', 'upload_date')
    list_filter = ('status', 'category', 'upload_date')
    search_fields = ('evidence_code', 'title', 'file_hash', 'description')
    readonly_fields = ('evidence_code', 'file_hash', 'file_size', 'upload_date')


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_id', 'evidence', 'admin', 'verification_status', 'verification_date')
    list_filter = ('verification_status', 'verification_date')
    search_fields = ('evidence__evidence_code', 'original_hash', 'current_hash', 'remarks')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'timestamp', 'user', 'action', 'evidence', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('action', 'details', 'user__username', 'evidence__evidence_code')
    readonly_fields = ('timestamp',)


@admin.register(EvidenceAccess)
class EvidenceAccessAdmin(admin.ModelAdmin):
    list_display = ('access_id', 'evidence', 'user', 'action', 'access_date')
    list_filter = ('action', 'access_date')
    search_fields = ('evidence__evidence_code', 'user__username')
