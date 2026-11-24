import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, FileResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from .models import Category, Evidence, Verification, AuditLog, EvidenceAccess
from .forms import EvidenceUploadForm, CategoryForm, EvidenceSearchForm
from accounts.models import User
from accounts.forms import AdminUserEditForm, RegisterForm
from . import services

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


# ==========================================================
# ADMIN MODULE VIEWS
# ==========================================================

@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted to administrators.')
        return redirect('user_dashboard')

    total_users = User.objects.count()
    total_evidence = Evidence.objects.count()
    verified_evidence = Evidence.objects.filter(status='Verified').count()
    pending_evidence = Evidence.objects.filter(status='Pending').count()
    rejected_evidence = Evidence.objects.filter(status='Rejected').count()

    recent_activities = AuditLog.objects.select_related('user', 'evidence')[:8]
    recent_evidence = Evidence.objects.select_related('category', 'user').order_by('-upload_date')[:6]
    pending_queue_items = Evidence.objects.filter(status='Pending').order_by('upload_date')[:5]

    # Category distribution for charts
    categories = Category.objects.annotate(ev_count=Count('evidences'))
    cat_names = [c.category_name for c in categories]
    cat_counts = [c.ev_count for c in categories]

    context = {
        'total_users': total_users,
        'total_evidence': total_evidence,
        'verified_evidence': verified_evidence,
        'pending_evidence': pending_evidence,
        'rejected_evidence': rejected_evidence,
        'recent_activities': recent_activities,
        'recent_evidence': recent_evidence,
        'pending_queue_items': pending_queue_items,
        'cat_names': cat_names,
        'cat_counts': cat_counts,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_manage_users(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted to administrators.')
        return redirect('user_dashboard')

    users = User.objects.all().order_by('-date_joined')

    # Add user form
    if request.method == 'POST' and 'add_user' in request.POST:
        create_form = RegisterForm(request.POST)
        if create_form.is_valid():
            new_user = create_form.save(commit=False)
            new_user.set_password(create_form.cleaned_data['password'])
            new_user.save()
            AuditLog.objects.create(
                user=request.user,
                action='ADMIN_USER_CREATE',
                details=f"Admin created account for {new_user.username} ({new_user.role})",
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"User {new_user.username} added successfully.")
            return redirect('admin_manage_users')
    else:
        create_form = RegisterForm()

    context = {
        'users': users,
        'create_form': create_form,
    }
    return render(request, 'admin/manage_users.html', context)


@login_required
def admin_toggle_user_status(request, user_id):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted.')
        return redirect('user_dashboard')

    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, 'You cannot deactivate your own administrative account.')
        return redirect('admin_manage_users')

    target_user.status = 'inactive' if target_user.status == 'active' else 'active'
    target_user.is_active = (target_user.status == 'active')
    target_user.save()

    AuditLog.objects.create(
        user=request.user,
        action='USER_STATUS_CHANGE',
        details=f"Changed status of {target_user.username} to {target_user.status}",
        ip_address=get_client_ip(request)
    )
    messages.success(request, f"User {target_user.username} is now {target_user.status.upper()}.")
    return redirect('admin_manage_users')


@login_required
def admin_all_evidence(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted.')
        return redirect('user_dashboard')

    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    search_q = request.GET.get('q')

    evidences = Evidence.objects.select_related('user', 'category').all()

    if category_filter:
        evidences = evidences.filter(category_id=category_filter)
    if status_filter:
        evidences = evidences.filter(status=status_filter)
    if search_q:
        evidences = evidences.filter(
            Q(title__icontains=search_q) |
            Q(evidence_code__icontains=search_q) |
            Q(description__icontains=search_q)
        )

    evidences = evidences.order_by('-upload_date')
    categories = Category.objects.all()

    context = {
        'evidences': evidences,
        'categories': categories,
        'current_category': category_filter,
        'current_status': status_filter,
        'search_q': search_q,
    }
    return render(request, 'admin/all_evidence.html', context)


@login_required
def admin_verify_evidence(request, evidence_id):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted to administrators.')
        return redirect('user_dashboard')

    evidence = get_object_or_404(Evidence.objects.select_related('user', 'category'), pk=evidence_id)

    # Perform Live Cryptographic SHA-256 Hash Verification
    is_valid, current_hash, original_hash, file_exists = services.verify_file_hash(evidence)

    if request.method == 'POST':
        action = request.POST.get('verification_action') # 'approve' or 'reject'
        remarks = request.POST.get('remarks', '').strip()

        if action == 'approve':
            if is_valid:
                evidence.status = 'Verified'
                verif_status = 'Verified'
                messages.success(request, f"Evidence {evidence.evidence_code} verified successfully! Cryptographic integrity confirmed.")
            else:
                evidence.status = 'Rejected'
                verif_status = 'Tampered'
                messages.error(request, f"INTEGRITY FAILED! File hash does not match original fingerprint.")
        else:
            evidence.status = 'Rejected'
            verif_status = 'Rejected'
            messages.info(request, f"Evidence {evidence.evidence_code} has been rejected.")

        evidence.save()

        # Log verification record
        Verification.objects.create(
            evidence=evidence,
            admin=request.user,
            original_hash=original_hash,
            current_hash=current_hash,
            verification_status=verif_status,
            remarks=remarks
        )

        AuditLog.objects.create(
            user=request.user,
            evidence=evidence,
            action=f"VERIFICATION_{verif_status.upper()}",
            details=f"Verification result: {verif_status}. Remarks: {remarks}",
            ip_address=get_client_ip(request)
        )

        return redirect('admin_all_evidence')

    verifications = evidence.verifications.select_related('admin').order_by('-verification_date')

    context = {
        'evidence': evidence,
        'is_valid': is_valid,
        'current_hash': current_hash,
        'original_hash': original_hash,
        'file_exists': file_exists,
        'verifications': verifications,
    }
    return render(request, 'admin/verify_evidence.html', context)


@login_required
def admin_categories(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted.')
        return redirect('user_dashboard')

    categories = Category.objects.annotate(total_files=Count('evidences')).order_by('category_id')

    if request.method == 'POST':
        if 'add_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                cat = form.save()
                AuditLog.objects.create(
                    user=request.user,
                    action='CATEGORY_CREATE',
                    details=f"Category '{cat.category_name}' created.",
                    ip_address=get_client_ip(request)
                )
                messages.success(request, f"Category '{cat.category_name}' created.")
                return redirect('admin_categories')
        elif 'delete_category' in request.POST:
            cat_id = request.POST.get('category_id')
            cat = get_object_or_404(Category, pk=cat_id)
            name = cat.category_name
            cat.delete()
            AuditLog.objects.create(
                user=request.user,
                action='CATEGORY_DELETE',
                details=f"Category '{name}' deleted.",
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Category '{name}' deleted.")
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'admin/categories.html', context)


@login_required
def admin_reports(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted.')
        return redirect('user_dashboard')

    total_evidence = Evidence.objects.count()
    verified_count = Evidence.objects.filter(status='Verified').count()
    pending_count = Evidence.objects.filter(status='Pending').count()
    rejected_count = Evidence.objects.filter(status='Rejected').count()

    categories = Category.objects.annotate(count=Count('evidences'))
    user_uploads = User.objects.annotate(upload_count=Count('evidences')).filter(upload_count__gt=0).order_by('-upload_count')[:10]
    recent_verifications = Verification.objects.select_related('evidence', 'admin').order_by('-verification_date')[:10]
    download_logs = EvidenceAccess.objects.filter(action='DOWNLOAD').select_related('evidence', 'user')[:15]

    context = {
        'total_evidence': total_evidence,
        'verified_count': verified_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'categories': categories,
        'user_uploads': user_uploads,
        'recent_verifications': recent_verifications,
        'download_logs': download_logs,
    }
    return render(request, 'admin/reports.html', context)


@login_required
def admin_audit_logs(request):
    if not request.user.is_admin():
        messages.warning(request, 'Access restricted.')
        return redirect('user_dashboard')

    action_filter = request.GET.get('action')
    logs = AuditLog.objects.select_related('user', 'evidence').all()

    if action_filter:
        logs = logs.filter(action__icontains=action_filter)

    logs = logs[:100]

    context = {
        'logs': logs,
        'action_filter': action_filter,
    }
    return render(request, 'admin/audit_logs.html', context)


# ==========================================================
# USER MODULE VIEWS
# ==========================================================

@login_required
def user_dashboard(request):
    user = request.user
    my_evidences = Evidence.objects.filter(user=user)
    total_uploaded = my_evidences.count()
    verified_count = my_evidences.filter(status='Verified').count()
    pending_count = my_evidences.filter(status='Pending').count()
    rejected_count = my_evidences.filter(status='Rejected').count()

    recent_uploads = my_evidences.select_related('category').order_by('-upload_date')[:6]
    system_categories = Category.objects.annotate(count=Count('evidences'))

    context = {
        'total_uploaded': total_uploaded,
        'verified_count': verified_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'recent_uploads': recent_uploads,
        'system_categories': system_categories,
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def user_upload_evidence(request):
    if request.method == 'POST':
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.user = request.user
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                evidence.file_type = uploaded_file.content_type
                evidence.file_size = uploaded_file.size
            evidence.status = 'Pending'
            evidence.save()

            AuditLog.objects.create(
                user=request.user,
                evidence=evidence,
                action='EVIDENCE_UPLOAD',
                details=f"Uploaded evidence {evidence.evidence_code}: '{evidence.title}'. Generated SHA-256: {evidence.file_hash}",
                ip_address=get_client_ip(request)
            )

            messages.success(request, f"Evidence '{evidence.title}' uploaded successfully! Recorded SHA-256: {evidence.file_hash[:16]}...")
            return redirect('evidence_details', evidence_id=evidence.evidence_id)
    else:
        form = EvidenceUploadForm()

    return render(request, 'user/upload_evidence.html', {'form': form})


@login_required
def user_my_evidence(request):
    evidences = Evidence.objects.filter(user=request.user).select_related('category').order_by('-upload_date')
    context = {
        'evidences': evidences,
    }
    return render(request, 'user/my_evidence.html', context)


@login_required
def evidence_search(request):
    form = EvidenceSearchForm(request.GET or None)
    results = []
    algorithm_info = None

    all_evidences = list(Evidence.objects.select_related('category', 'user').all())

    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        cat = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        algo = form.cleaned_data.get('algorithm', 'c_binary')

        # Filter pool if category or status selected
        pool = all_evidences
        if cat:
            pool = [e for e in pool if e.category == cat]
        if status:
            pool = [e for e in pool if e.status == status]

        if query:
            # C Algorithm Integration
            if algo == 'c_hash':
                # Use Hash Table O(1) lookup
                clean_query = query.upper()
                c_res = services.run_hash_table(pool, search_code=clean_query)
                algorithm_info = c_res
                if c_res.get('search') and c_res['search'].get('item'):
                    target_id = c_res['search']['item']['id']
                    results = [e for e in pool if e.evidence_id == target_id]
            elif algo == 'c_bst':
                # Use BST lookup
                search_id = None
                if query.isdigit():
                    search_id = int(query)
                elif query.startswith('E') and query[1:].isdigit():
                    search_id = int(query[1:]) - 100
                c_res = services.run_bst(pool, search_id=search_id)
                algorithm_info = c_res
                if c_res.get('search') and c_res['search'].get('item'):
                    target_id = c_res['search']['item']['id']
                    results = [e for e in pool if e.evidence_id == target_id]
            elif algo == 'c_linear':
                # Linear Search on title/code
                c_res = services.run_search(pool, query=query, search_type='linear')
                algorithm_info = c_res
                if c_res.get('item'):
                    target_id = c_res['item']['id']
                    results = [e for e in pool if e.evidence_id == target_id]
                else:
                    # Broad fallback search
                    results = [e for e in pool if query.lower() in e.title.lower() or query.lower() in (e.evidence_code or '').lower()]
            else: # c_binary
                # Binary Search on sorted ID
                search_id = None
                if query.isdigit():
                    search_id = int(query)
                elif query.startswith('E') and query[1:].isdigit():
                    search_id = int(query[1:]) - 100
                else:
                    # If query is text, use linear search
                    search_id = -1

                if search_id and search_id > 0:
                    c_res = services.run_search(pool, query=str(search_id), search_type='binary')
                    algorithm_info = c_res
                    if c_res.get('item'):
                        target_id = c_res['item']['id']
                        results = [e for e in pool if e.evidence_id == target_id]
                else:
                    results = [e for e in pool if query.lower() in e.title.lower() or query.lower() in (e.evidence_code or '').lower()]
                    algorithm_info = {
                        "algorithm": "C Algorithm Search & Substring Match",
                        "query": query,
                        "comparisons": len(pool),
                        "found": len(results) > 0
                    }
        else:
            results = pool
    else:
        results = all_evidences

    context = {
        'form': form,
        'results': results,
        'algorithm_info': algorithm_info,
    }
    return render(request, 'user/search_evidence.html', context)


@login_required
def evidence_details(request, evidence_id):
    evidence = get_object_or_404(Evidence.objects.select_related('user', 'category'), pk=evidence_id)

    # Record access
    EvidenceAccess.objects.create(
        evidence=evidence,
        user=request.user,
        action='VIEW'
    )

    verifications = evidence.verifications.select_related('admin').order_by('-verification_date')
    access_logs = evidence.access_records.select_related('user').order_by('-access_date')[:10]

    context = {
        'evidence': evidence,
        'verifications': verifications,
        'access_logs': access_logs,
    }
    return render(request, 'user/evidence_details.html', context)


@login_required
def evidence_download(request, evidence_id):
    evidence = get_object_or_404(Evidence, pk=evidence_id)

    # Permission check: Admin or the owner can download, or if status is Verified
    if not (request.user.is_admin() or evidence.user == request.user or evidence.status == 'Verified'):
        messages.error(request, 'Access Denied: You are not authorized to download this unverified evidence.')
        return redirect('evidence_details', evidence_id=evidence.evidence_id)

    if not evidence.file or not os.path.exists(evidence.file.path):
        raise Http404("Evidence file is not present on storage.")

    # Record Download Access
    EvidenceAccess.objects.create(
        evidence=evidence,
        user=request.user,
        action='DOWNLOAD'
    )

    AuditLog.objects.create(
        user=request.user,
        evidence=evidence,
        action='EVIDENCE_DOWNLOAD',
        details=f"User {request.user.username} downloaded evidence file {os.path.basename(evidence.file.name)}",
        ip_address=get_client_ip(request)
    )

    response = FileResponse(open(evidence.file.path, 'rb'), as_attachment=True, filename=os.path.basename(evidence.file.name))
    return response


@login_required
def user_upload_history(request):
    evidences = Evidence.objects.filter(user=request.user).select_related('category').order_by('-upload_date')
    accesses = EvidenceAccess.objects.filter(user=request.user).select_related('evidence').order_by('-access_date')[:20]

    context = {
        'evidences': evidences,
        'accesses': accesses,
    }
    return render(request, 'user/upload_history.html', context)


# ==========================================================
# C DATA STRUCTURES LIVE VISUALIZER VIEW
# ==========================================================

@login_required
def data_structures_hub(request):
    """
    Dedicated interactive showcase demonstrating all C data structures:
    1. Linked List
    2. Hash Table
    3. Binary Search Tree
    4. Queue (FIFO)
    5. Sorting (QuickSort)
    """
    evidences = list(Evidence.objects.select_related('category').all().order_by('evidence_id'))

    sort_field = request.GET.get('sort_field', 'id')
    sort_order = request.GET.get('sort_order', 'asc')
    search_key = request.GET.get('search_key', 'E101')

    # Execute all C algorithms
    linked_list_data = services.run_linked_list(evidences)
    hash_table_data = services.run_hash_table(evidences, search_code=search_key)
    bst_data = services.run_bst(evidences, search_id=101)
    queue_data = services.run_queue([e for e in evidences if e.status == 'Pending'] or evidences)
    sorting_data = services.run_sorting(evidences, field=sort_field, order=sort_order)

    context = {
        'evidences': evidences,
        'linked_list_data': linked_list_data,
        'hash_table_data': hash_table_data,
        'bst_data': bst_data,
        'queue_data': queue_data,
        'sorting_data': sorting_data,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'search_key': search_key,
    }
    return render(request, 'data_structures.html', context)
