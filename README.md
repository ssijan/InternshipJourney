## NB: drf_permissions app is for my practice only

# Secure DRF Ledger & RBAC Architecture Microservice

This repository implements a production-hardened, enterprise-grade Role-Based Access Control (RBAC) and Row-Level Security (RLS) system built on Django REST Framework (DRF), SimpleJWT, and Django-Guardian.

The design targets defensive architectures meant to withstand high-concurrency environments and aggressive external application penetration mapping by eliminating common OWASP API hazards like **BOLA / IDOR (Broken Object Level Authorization)**.

---

## 🛠️ System Architecture & Core Mechanics

The authorization pipeline leverages stateless JWT claims for global checks, paired with defensive query filtering to enforce strict resource isolation.

### The Request Security Lifecycle
1. **Cryptographic Validation**: `SimpleJWT` verifies the signature of incoming `Authorization: Bearer <token>` payloads.
2. **Stateless Claim Extraction**: Roles and verification states are parsed into memory via `request.auth`, avoiding heavy database hits during early authorization phases.
3. **Global Composition Gate**: The view evaluates permissions via sequential bitwise logic (`&` and `|`).
4. **Row-Level Sandbox**: `get_queryset()` strictly bounds the evaluation context to the user's specific ownership domain before an object lookup is completed.

---

## 📋 Permission Matrix Documentation

The following matrix documents the definitive system states enforced across every endpoint. BOLA-targeted requests are terminated via `HTTP 404 Not Found` rather than a `403 Forbidden` to limit architectural discovery leaks.

| Endpoint Route | HTTP Method | System Action | ADMIN | AGENT | CUSTOMER (Owner) | CUSTOMER (Non-Owner) | Underlying Security Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/transactions/` | `GET` | List entries | ✅ Allow (All Rows) | ✅ Allow (All Rows) | 🔒 Filtered (Own Rows) | ❌ Deny (Empty List) | QuerySet Separation Sandbox |
| `/api/v1/transactions/` | `POST` | Create record | ✅ Allow | ✅ Allow | ✅ Allow | ✅ Allow | Context Serializer User Injection |
| `/api/v1/transactions/{id}/` | `GET` | Retrieve record | ✅ Allow | ✅ Allow | ✅ Allow | ❌ **404 Not Found** | Database QuerySet Exclusion Bound |
| `/api/v1/transactions/{id}/` | `PUT/PATCH` | Modify entry | ✅ Allow | ✅ Allow | ❌ Deny (Read Only) | ❌ **404 Not Found** | Serializer Read Only / Permissions |
| `/api/v1/transactions/{id}/dispute/` | `POST` | Dispute record | ✅ Allow | ✅ Allow | ✅ Allow | ❌ **404 Not Found** | `get_object()` Object-Level Gate |

---

## 🚀 Deployment & Installation

### 1. Environment Setup
Clone the repository and install the required dependencies:
```bash
pip install django djangorestframework djangorestframework-simplejwt django-guardian

```

### Author
```
Md. Sakibur Rahman
```