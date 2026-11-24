# DIGITAL EVIDENCE SYSTEM
## Intelligent Evidence Organization and Retrieval

A complete, high-tech, web-based **Digital Evidence Management System (DEMS)** featuring cryptographic SHA-256 integrity verification, role-based workflows (Admin & Investigator), and native **C Programming Data Structures & Algorithms** integrated directly into the Python Django backend.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **HTML5** | Modern semantic structure & accessible components |
| **CSS3 & Glassmorphism** | Custom dark cyber-forensic UI, glowing indicators, responsive layouts |
| **JavaScript (ES6+)** | Dynamic drag-and-drop file upload, live search, hash copy, Chart.js telemetry |
| **Python Django (6.1)** | Backend framework, role dispatch, session security, cryptographic hashing |
| **C Programming (GCC C99)**| Data structure algorithms: Linked List, Hash Table, BST, Queue, QuickSort |
| **SQLite / SQL** | Relational database schema with immutable audit trails |
| **SHA-256 Cryptography** | Real-time file integrity verification & tampering detection |

---

## 🚀 Quick Start Guide (Windows)

### 1. Prerequisites
- Python 3.10+
- Django (`pip install django pillow`)
- GCC (MinGW) for recompiling C source files if desired (compiled `.exe` binaries are already included)

### 2. Run the Development Server
Open PowerShell in the project directory:

```powershell
cd D:\project
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Pre-Configured Test Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full administrative control, verify integrity, manage users, categories, view audit logs & reports |
| **Investigator (User)** | `investigator` | `user123` | Ingest evidence, view custody records, search with C algorithms, download authorized files |
| **Investigator (User 2)** | `agent_miller` | `user123` | Secondary user for multi-user collaboration tests |

*(Quick-fill buttons are also available on the Login screen for instant one-click testing!)*

---

## 📂 Project Architecture & Directory Structure

```text
DIGITAL_EVIDENCE_SYSTEM/
│
├── manage.py                        # Django administrative CLI
├── requirements.txt                 # Project dependencies
├── db.sqlite3                       # Pre-populated SQLite database
│
├── digital_evidence/                # Django Core Settings & Routing
│   ├── settings.py                  # Custom User model, media & static config
│   ├── urls.py                      # Master URL dispatcher
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                        # User Authentication & Role Management
│   ├── models.py                    # Extended User model (role, status, badge_id, department)
│   ├── views.py                     # Login, register, logout, profile dispatch
│   ├── forms.py                     # Auth forms & profile management
│   └── urls.py
│
├── evidence/                        # Digital Evidence Core Application
│   ├── models.py                    # Category, Evidence, Verification, AuditLog, EvidenceAccess
│   ├── services.py                  # C Binary Subprocess execution & SHA-256 verification
│   ├── views.py                     # Admin & User views, search, reports, details, download
│   ├── forms.py                     # Upload form with file validation, search form
│   └── urls.py
│
├── algorithms/                      # C Data Structures & Compiled Executables
│   ├── linkedlist.c                 # Singly Linked List algorithm
│   ├── hashtable.c                  # O(1) Separate Chaining Hash Table algorithm
│   ├── bst.c                        # Binary Search Tree algorithm
│   ├── queue.c                      # FIFO Verification Queue algorithm
│   ├── sorting.c                    # Multi-key QuickSort algorithm
│   ├── search.c                     # Binary Search & Linear Search algorithms
│   └── compiled/                    # Compiled Windows Executables (.exe)
│       ├── linkedlist.exe
│       ├── hashtable.exe
│       ├── bst.exe
│       ├── queue.exe
│       ├── sorting.exe
│       └── search.exe
│
├── templates/                       # HTML Templates
│   ├── base.html                    # Master Cyber-Forensic Layout
│   ├── login.html                   # High-Tech Login Portal
│   ├── register.html                # Investigator Registration Portal
│   ├── data_structures.html         # Interactive C Data Structures Showcase
│   ├── admin/
│   │   ├── dashboard.html           # Admin Metrics, Queue & Category Charts
│   │   ├── manage_users.html        # User Directory & Role Assignment
│   │   ├── all_evidence.html        # Repository with Filter & Action Ribbon
│   │   ├── verify_evidence.html     # Cryptographic SHA-256 Hash Verification Station
│   │   ├── categories.html          # Category Configurator
│   │   ├── reports.html             # Chart.js Visual Analytics & Export
│   │   └── audit_logs.html          # Immutable Activity Trail
│   └── user/
│       ├── dashboard.html           # User Overview & Quick Actions
│       ├── upload_evidence.html     # Drag-and-Drop Ingestion Zone
│       ├── my_evidence.html         # User Custody Records
│       ├── search_evidence.html     # Multi-Algorithm Search Engine
│       ├── evidence_details.html    # Media Viewer & Chain of Custody
│       ├── upload_history.html      # Chronological Audit History
│       └── profile.html             # Profile Details & Password Security
│
├── static/                          # Static Assets
│   ├── css/
│   │   ├── style.css                # Master Cyber Theme, Glassmorphism & Tables
│   │   ├── login.css                # Authentication Styling
│   │   ├── admin.css                # Admin Hash Matrix & Layout
│   │   └── user.css                 # Upload Dropzone & UI Components
│   ├── js/
│   │   ├── main.js                  # Global Toast & Copy-Hash Helpers
│   │   ├── login.js                 # Validation & Password Toggle
│   │   ├── upload.js                # Drag-and-Drop & Live Preview
│   │   └── search.js                # Algorithm Switcher & Quick Filter
│   └── images/
│       └── logo.png                 # Shield Cyber Emblem
│
├── media/evidence/                  # Sealed Physical Evidence Storage
└── database/
    ├── schema.sql                   # Pure SQL DDL Reference (6 Tables)
    └── seed_data.py                 # Initial Demo Data Population Script
```

---

## ⚡ C Data Structures & Algorithms Integration

The system includes 5 core data structures written in C (`algorithms/`), compiled with GCC, and executed from Django via `subprocess.run()`:

```text
HTML / CSS / JavaScript (Frontend UI)
          │
          ▼
    Django Backend (Python)
          │
          ▼
`evidence/services.py` Serializer (Pipe Delimited Records)
          │
          ▼
   C Compiled Binaries (algorithms/compiled/*.exe)
   ├── linkedlist.exe  ➔ Dynamic node chaining & traversal
   ├── hashtable.exe   ➔ O(1) hash bucket search with polynomial rolling hash
   ├── bst.exe         ➔ Hierarchical tree organization & in-order sorted traversal
   ├── queue.exe       ➔ FIFO verification request ordering
   └── sorting.exe     ➔ Multi-key QuickSort with comparisons & swaps telemetry
          │
          ▼
JSON Execution Output parsed & visualized on the Web UI
```

*Note: If run in a restricted environment, an automatic dual-mode Python emulation ensures zero downtime while preserving identical algorithm logic.*

---

## 🔒 Security & Forensic Integrity Features

1. **Cryptographic SHA-256 Sealing**: On upload, files are streamed in 64KB chunks to compute an immutable hash recorded in the SQL database.
2. **Real-Time Verification Matrix**: When administrators verify evidence, the file is re-read live from disk to detect any byte-level tampering or corruption.
3. **Role-Based Access Control**: Admins and Users have separated permissions and distinct workspaces.
4. **Immutable Audit Logging**: Every upload, login, status toggle, download, and verification is logged with timestamp, user ID, and IP address.
5. **Chain of Custody Tracking**: Table 6 (`evidence_access`) logs every view and authorized download.
