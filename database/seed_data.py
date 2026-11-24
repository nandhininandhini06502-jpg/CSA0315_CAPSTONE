import os
import sys
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_evidence.settings')

import django
django.setup()

from django.core.files.base import ContentFile
from accounts.models import User
from evidence.models import Category, Evidence, Verification, AuditLog, EvidenceAccess

def seed():
    print("🌱 Starting database population for Digital Evidence System...")

    # 1. Create Categories
    categories_data = [
        ("Image Evidence", "Photographic crime scene captures, surveillance frames, biometric photos", "fa-image"),
        ("Video Evidence", "CCTV video streams, body-worn camera captures, traffic footage", "fa-video"),
        ("Audio Evidence", "911 emergency calls, wiretaps, suspect interview audio recordings", "fa-microphone-lines"),
        ("Document Evidence", "Autopsy reports, search warrants, forensic laboratory statements", "fa-file-pdf"),
        ("Other Digital Evidence", "RAM captures, forensic disk dumps, PCAP network traffic", "fa-hard-drive")
    ]

    cat_objs = {}
    for name, desc, icon in categories_data:
        cat, created = Category.objects.get_or_create(
            category_name=name,
            defaults={'description': desc, 'icon': icon}
        )
        cat_objs[name] = cat
        print(f"  Category: {name} (Created: {created})")

    # 2. Create Default Users
    # Admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@forensic.gov',
            'first_name': 'Chief',
            'last_name': 'Administrator',
            'role': 'admin',
            'status': 'active',
            'department': 'Forensic Command Directorate',
            'badge_id': 'DIR-001',
            'phone': '+1 (555) 019-2831',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created or not admin_user.check_password('admin123'):
        admin_user.set_password('admin123')
        admin_user.save()
    print(f"  Admin User: {admin_user.username} (Password: admin123)")

    # Investigator User
    inv_user, created = User.objects.get_or_create(
        username='investigator',
        defaults={
            'email': 'investigator@forensic.gov',
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'role': 'user',
            'status': 'active',
            'department': 'Cyber Crime Forensics Unit',
            'badge_id': 'INV-402',
            'phone': '+1 (555) 019-7492'
        }
    )
    if created or not inv_user.check_password('user123'):
        inv_user.set_password('user123')
        inv_user.save()
    print(f"  Investigator User: {inv_user.username} (Password: user123)")

    # Investigator User 2
    inv_user2, created = User.objects.get_or_create(
        username='agent_miller',
        defaults={
            'email': 'miller@forensic.gov',
            'first_name': 'Marcus',
            'last_name': 'Miller',
            'role': 'user',
            'status': 'active',
            'department': 'Field Investigation Squad',
            'badge_id': 'INV-309',
            'phone': '+1 (555) 019-8812'
        }
    )
    if created or not inv_user2.check_password('user123'):
        inv_user2.set_password('user123')
        inv_user2.save()
    print(f"  Investigator User 2: {inv_user2.username} (Password: user123)")

    # 3. Create Sample Evidence Files in media/evidence/
    media_ev_dir = BASE_DIR / 'media' / 'evidence'
    media_ev_dir.mkdir(parents=True, exist_ok=True)

    evidence_samples = [
        {
            "code": "E101",
            "title": "Intersection_Traffic_Accident_Angle1.jpg",
            "description": "High-resolution photographic capture of traffic collision scene at 5th Ave intersection.",
            "category": cat_objs["Image Evidence"],
            "user": inv_user,
            "filename": "E101_Intersection_Traffic_Accident_Angle1.jpg",
            "file_type": "image/jpeg",
            "status": "Verified",
            "make_file": "image"
        },
        {
            "code": "E102",
            "title": "Forensic_Autopsy_Toxicology_Report.pdf",
            "description": "Certified medical examiner report detailing chemical blood screen analysis.",
            "category": cat_objs["Document Evidence"],
            "user": inv_user,
            "filename": "E102_Forensic_Autopsy_Toxicology_Report.pdf",
            "file_type": "application/pdf",
            "status": "Verified",
            "make_file": "pdf"
        },
        {
            "code": "E103",
            "title": "CCTV_Vault_North_Corridor.mp4",
            "description": "1080p surveillance video snippet recorded from security camera #4 showing vault access.",
            "category": cat_objs["Video Evidence"],
            "user": inv_user2,
            "filename": "E103_CCTV_Vault_North_Corridor.mp4",
            "file_type": "video/mp4",
            "status": "Pending",
            "make_file": "video"
        },
        {
            "code": "E104",
            "title": "Emergency_Dispatch_Call_911.mp3",
            "description": "Emergency 911 dispatch voice recording logged at 02:44 AM from caller reporting distress.",
            "category": cat_objs["Audio Evidence"],
            "user": inv_user,
            "filename": "E104_Emergency_Dispatch_Call_911.mp3",
            "file_type": "audio/mpeg",
            "status": "Pending",
            "make_file": "audio"
        },
        {
            "code": "E105",
            "title": "Suspect_Laptop_RAM_Volatile_Dump.raw",
            "description": "Physical volatile memory raw dump extracted via hardware DMA tool during search warrant.",
            "category": cat_objs["Other Digital Evidence"],
            "user": inv_user2,
            "filename": "E105_Suspect_Laptop_RAM_Volatile_Dump.raw",
            "file_type": "application/octet-stream",
            "status": "Verified",
            "make_file": "binary"
        }
    ]

    for item in evidence_samples:
        file_path = media_ev_dir / item["filename"]
        
        # Generate genuine file bytes
        if item["make_file"] == "image":
            img = Image.new('RGB', (640, 480), color=(15, 23, 42))
            d = ImageDraw.Draw(img)
            d.rectangle([(20, 20), (620, 460)], outline=(56, 189, 248), width=3)
            d.text((40, 50), f"EVIDENCE ARCHIVE: {item['code']}", fill=(255, 255, 255))
            d.text((40, 80), f"Title: {item['title']}", fill=(56, 189, 248))
            d.text((40, 110), f"Chain of Custody: {item['user'].username}", fill=(148, 163, 184))
            img.save(file_path, "JPEG")
        elif item["make_file"] == "pdf":
            # Simple valid PDF binary header
            pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Forensic Autopsy Report) /Author (Medical Examiner) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"
            file_path.write_bytes(pdf_content)
        else:
            dummy_bytes = f"DIGITAL FORENSIC EVIDENCE ARTIFACT {item['code']} - {item['title']}\nSEALED UNDER FEDERAL CHAIN OF CUSTODY RULES\n".encode('utf-8')
            dummy_bytes += os.urandom(1024 * 4) # 4KB artifact
            file_path.write_bytes(dummy_bytes)

        # Calculate exact SHA-256
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        calc_hash = sha256.hexdigest()
        file_size = file_path.stat().st_size

        rel_path = f"evidence/{item['filename']}"

        ev, created = Evidence.objects.get_or_create(
            evidence_code=item["code"],
            defaults={
                'title': item["title"],
                'description': item["description"],
                'category': item["category"],
                'user': item["user"],
                'file': rel_path,
                'file_type': item["file_type"],
                'file_size': file_size,
                'file_hash': calc_hash,
                'status': item["status"]
            }
        )

        if not created:
            ev.file = rel_path
            ev.file_hash = calc_hash
            ev.file_size = file_size
            ev.status = item["status"]
            ev.save()

        print(f"  Evidence: {ev.evidence_code} - {ev.title} (SHA-256: {calc_hash[:16]}...)")

        # Create Verification Record if Verified
        if ev.status == 'Verified':
            Verification.objects.get_or_create(
                evidence=ev,
                admin=admin_user,
                defaults={
                    'original_hash': calc_hash,
                    'current_hash': calc_hash,
                    'verification_status': 'Verified',
                    'remarks': 'Bit-level cryptographic SHA-256 match confirmed. Forensic integrity intact.'
                }
            )

        # Audit Log
        AuditLog.objects.create(
            user=item["user"],
            evidence=ev,
            action='EVIDENCE_INGESTED',
            details=f"Evidence {ev.evidence_code} uploaded and indexed.",
            ip_address="127.0.0.1"
        )

        # Access record
        EvidenceAccess.objects.create(
            evidence=ev,
            user=item["user"],
            action='VIEW'
        )

    print(" Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
