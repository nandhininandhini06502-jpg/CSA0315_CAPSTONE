from django.urls import path
from . import views

urlpatterns = [
    # Admin Views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin-dashboard/users/<int:user_id>/toggle/', views.admin_toggle_user_status, name='admin_toggle_user_status'),
    path('admin-dashboard/evidence/', views.admin_all_evidence, name='admin_all_evidence'),
    path('admin-dashboard/verify/<int:evidence_id>/', views.admin_verify_evidence, name='admin_verify_evidence'),
    path('admin-dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('admin-dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('admin-dashboard/audit-logs/', views.admin_audit_logs, name='admin_audit_logs'),

    # User Views
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('upload/', views.user_upload_evidence, name='user_upload_evidence'),
    path('my-evidence/', views.user_my_evidence, name='user_my_evidence'),
    path('search/', views.evidence_search, name='evidence_search'),
    path('evidence/<int:evidence_id>/', views.evidence_details, name='evidence_details'),
    path('evidence/<int:evidence_id>/download/', views.evidence_download, name='evidence_download'),
    path('history/', views.user_upload_history, name='user_upload_history'),

    # C Algorithms Showcase
    path('algorithms-hub/', views.data_structures_hub, name='data_structures_hub'),
]
