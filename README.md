# Multi-Paradigm Authentication & Session Tracking System

An advanced identity management and security architecture built with **Django REST Framework (DRF)** and **SimpleJWT**. This project was engineered to demonstrate a deep understanding of stateless vs. stateful authentication, custom cryptographic token claims, custom case-insensitive backends, and precise user session device tracking/revocation workflows.

---

## 🏗️ System Architecture & Workflow

The platform implements a hybrid security model: **Stateless validation** for rapid API calls via short-lived Access Tokens, combined with **Stateful validation** for token refresh operations. This ensures zero database overhead for 95%+ of operations while retaining total system control over session revocation.

### Core Architecture Capabilities
* 🔄 **Refresh Token Rotation (RTR):** One-time use refresh tokens to prevent replay attacks.
* 🛡️ **Cryptographic Blacklisting:** Instant token invalidation upon explicit logout or administrative revocation.
* 📍 **Device Footprint Tracking:** Captures Client IP, User-Agent, and timestamps to track active logged-in locations.
* 🔑 **Custom Identity Layer:** Eradicates standard username configurations to prioritize secure email-based authentication.

---

## 📂 Repository File Map

```text
my_project/
│
├── core/                         # Global Configuration Engine
│   ├── settings.py               # Security configurations, SimpleJWT parameters
│   └── urls.py                   # Master routing dispatcher
│
├── authentication/               # Modular Authentication Context App
│   ├── backends.py               # Custom Case-Insensitive Email Verification Engine
│   ├── models.py                 # Core Custom User & Session Registry tables
│   ├── serializers.py            # Custom claims injectors & validation hooks
│   ├── views.py                  # Low-Level pure APIViews for all endpoints
│   └── urls.py                   # App-specific API endpoint definitions
│
└── manage.py

```

---

## 🛠️ Installation & Backend Setup

### 1. Environment Setup

Clone the repository and build a clean python environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

### 2. Dependency Installation

Install Django, DRF, and the core JWT cryptography libraries:

```bash
pip install django djangorestframework djangorestframework-simplejwt PyJWT

```

### 3. Database Initializations & System Migrations

Generate database tables for your custom user model, tracking indexes, and SimpleJWT outstanding token registries:

```bash
python manage.py makemigrations authentication
python manage.py migrate

```

### 4. Boot Up the Development Application Server

```bash
python manage.py runserver

```

---

## 🚀 API Endpoint Reference Matrix

| Action | HTTP Method | Endpoint Route | Protection Level | Description |
| --- | --- | --- | --- | --- |
| **Register** | `POST` | `/api/auth/register/` | `AllowAny` | Registers user using email; appends custom internal `account_id`. |
| **Login** | `POST` | `/api/auth/login/` | `AllowAny` | Evaluates email/password; signs claims; generates tokens & records session. |
| **Refresh** | `POST` | `/api/auth/refresh/` | `AllowAny` | Consumes valid refresh token; rotates token family; returns brand new pair. |
| **Logout** | `POST` | `/api/auth/logout/` | `AllowAny` | Explicitly invalidates the passed refresh token globally. |
| **List Sessions** | `GET` | `/api/auth/sessions/` | `IsAuthenticated` | Returns array of all current active user device footprints. |
| **Revoke Session** | `POST` | `/api/auth/sessions/<id>/revoke/` | `IsAuthenticated` | Target blacklists a specific token instance via its primary tracking ID. |
| **DRF Token Debug** | `POST` | `/api/auth/debug-drf-token/` | `IsAuthenticated` | Generates a stateful DRF static token for Task 1 validation tests. |

---

## 🧪 Postman & cURL Integration Testing Guide

### 1. User Registration Flow

```bash
curl -X POST [http://127.0.0.1:8000/api/auth/register/](http://127.0.0.1:8000/api/auth/register/) \
     -H "Content-Type: application/json" \
     -d '{"email": "intern@company.com", "password": "SecurePassword2026", "role": "engineer"}'

```

### 2. Login & Claims Generation Check

Submit a login request. The response contains both an `access` and `refresh` token. Copy the access token and paste it into [jwt.io](https://jwt.io) to visually confirm your custom claims (`role`, `account_id`) are cryptographically bound to the payload.

```bash
curl -X POST [http://127.0.0.1:8000/api/auth/login/](http://127.0.0.1:8000/api/auth/login/) \
     -H "Content-Type: application/json" \
     -d '{"email": "intern@company.com", "password": "SecurePassword2026"}'

```

### 3. Fetching Active User Sessions

Pass the access token inside the request header to inspect your device login logs.

```bash
curl -X GET [http://127.0.0.1:8000/api/auth/sessions/](http://127.0.0.1:8000/api/auth/sessions/) \
     -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN_HERE>"

```

### 4. Specific Session Revocation Verification

Target an active session ID returned from the previous request to destroy its authorization privileges.

```bash
curl -X POST [http://127.0.0.1:8000/api/auth/sessions/1/revoke/](http://127.0.0.1:8000/api/auth/sessions/1/revoke/) \
     -H "Authorization: Bearer <PASTE_YOUR_ACCESS_TOKEN_HERE>"

```

---

## 🔒 Security Posture & Standards Applied

* **Timing Attack Neutralization:** The custom authentication backend runs a placeholder password hash sequence (`User().set_password()`) if an email look-up fails. This forces uniform server response durations, breaking automated email gathering scripts.
* **Data Isolation Enforcement:** The token revocation view uses explicit query limits (`UserSessionTracker.objects.get(id=pk, user=request.user)`) preventing authenticated users from guessing or revoking sessions that belong to other user groups.
* **Token Rotation Defenses:** If an attacker intercepts a rotated refresh token and submits it a second time, SimpleJWT flags the duplicate usage anomaly, instantly blocking downstream generation requests.


## Author

```
Md. Sakibur Rahman
```