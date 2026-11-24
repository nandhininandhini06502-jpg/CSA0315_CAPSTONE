-- ==========================================================
-- DIGITAL EVIDENCE MANAGEMENT SYSTEM (DEMS)
-- Intelligent Evidence Organization and Retrieval
-- SQL Database Schema (Compatible with SQLite and MySQL)
-- ==========================================================

-- Table 1: Categories
CREATE TABLE IF NOT EXISTS evidence_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'fa-folder',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Users (Custom User Model)
CREATE TABLE IF NOT EXISTS accounts_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    role VARCHAR(20) NOT NULL DEFAULT 'user', -- 'admin' or 'user'
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- 'active' or 'inactive'
    department VARCHAR(100) DEFAULT 'Forensics & Investigation',
    badge_id VARCHAR(50) DEFAULT '',
    phone VARCHAR(20) DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    last_login DATETIME,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Digital Evidence
CREATE TABLE IF NOT EXISTS evidence_evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_code VARCHAR(20) UNIQUE, -- e.g. E101, E102
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER,
    file VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT DEFAULT 0,
    file_hash VARCHAR(64) NOT NULL, -- Cryptographic SHA-256 Digest
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending', -- 'Pending', 'Verified', 'Rejected'
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES evidence_category(category_id) ON DELETE SET NULL
);

-- Table 4: Verification (Integrity & Tampering Log)
CREATE TABLE IF NOT EXISTS evidence_verification (
    verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id INTEGER NOT NULL,
    admin_id INTEGER,
    original_hash VARCHAR(64) NOT NULL,
    current_hash VARCHAR(64) NOT NULL,
    verification_status VARCHAR(20) NOT NULL, -- 'Verified', 'Tampered', 'Rejected'
    remarks TEXT,
    verification_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evidence_id) REFERENCES evidence_evidence(evidence_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES accounts_user(id) ON DELETE SET NULL
);

-- Table 5: Audit Logs (Immutable Activity Trail)
CREATE TABLE IF NOT EXISTS evidence_auditlog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    evidence_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    ip_address VARCHAR(45),
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE SET NULL,
    FOREIGN KEY (evidence_id) REFERENCES evidence_evidence(evidence_id) ON DELETE SET NULL
);

-- Table 6: Evidence Access Logs
CREATE TABLE IF NOT EXISTS evidence_evidenceaccess (
    access_id INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL DEFAULT 'VIEW', -- 'VIEW', 'DOWNLOAD', 'VERIFY'
    access_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evidence_id) REFERENCES evidence_evidence(evidence_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- Indexes for Fast Retrieval
CREATE INDEX IF NOT EXISTS idx_evidence_code ON evidence_evidence(evidence_code);
CREATE INDEX IF NOT EXISTS idx_evidence_status ON evidence_evidence(status);
CREATE INDEX IF NOT EXISTS idx_evidence_category ON evidence_evidence(category_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON evidence_auditlog(timestamp);
