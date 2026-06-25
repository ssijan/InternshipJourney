# Task : Comparative Architectural Analysis — Stateful vs. Stateless Auth

This document provides a technical comparison between Django REST Framework's native, database-backed `TokenAuthentication` and the `django-rest-framework-simplejwt` implementation of `JWTAuthentication` evaluated side-by-side.

---

## 🏗️ Structural and Architectural Comparison

| Security and Performance Primitives | DRF Token Authentication (`TokenAuthentication`) | SimpleJWT Authentication (`JWTAuthentication`) |
| :--- | :--- | :--- |
| **State Management** | **Stateful:** The server holds the ground truth in the application database (`authtoken_token` table). | **Stateless:** The server holds nothing regarding active sessions; tokens are cryptographically self-contained. |
| **Verification Latency** | **High Overhead:** Requires a relational database query lookup on *every single incoming API request* to parse credentials. | **Low Overhead:** Handled via rapid, in-memory cryptographic signature verification; zero initial DB strain. |
| **Session Invalidation** | **Instantaneous:** Deleting the token row from the database invalidates the session globally across all systems. | **Deferred/Complex:** Tokens remain valid until their expiration timestamp (`exp`) passes unless explicit blacklists are checked. |
| **Payload Content** | **Opaque Hash:** Contains only a static key string pointing to a user record. No native metadata capacity. | **Structured JSON:** Contains metadata assertions (claims) including user permissions, role, and expirations. |
| **Horizontal Scalability** | **Difficult:** Requires sticky routing sessions or a highly available centralized database cluster across regions. | **Trivial:** Decoupled microservices can verify identity autonomously if they share the cryptographic key/secret. |

---

## 📊 Request and Response Lifecycle Flows

### 1. DRF Token Authentication (Stateful Lifecycle)


```

Client App                   API Gateway / DRF View                Database Layer
│                                  │                                  │
├─► [API Request + Token Key] ────►┤                                  │
│                                  ├─► [SQL: SELECT * FROM tokens] ──►┤
│                                  ◄─ [Returns Matching User Row] ────┤
│                                  │                                  │
◄─ [HTTP 200 OK / Response] ───────┴                                  │

```

### 2. SimpleJWT Authentication (Stateless Lifecycle)


```

Client App                   API Gateway / DRF View                Database Layer
│                                  │                                  │
├─► [API Request + Bearer JWT] ───►┤                                  │
│                                  ├─► [In-Memory Signature Match]    │ (No DB Trip
│                                  │   [Extract user_id & role]       │  for Identity
│                                  │                                  │  Verification)
◄─ [HTTP 200 OK / Response] ───────┴                                  │

```

---

## 🧪 Postman & cURL Verification Observations

During local execution verification tests on the endpoints, the following physical discrepancies were analyzed:

### 1. Standard DRF Token Output (From POST `/api/auth/debug-drf-token/`)
* **Token Shape:** A short, static alphanumeric string: `9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`.
* **Postman Header Syntax:**
  ```http
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

```

### 2. SimpleJWT Token Output (From POST `/api/auth/login/`)

* **Token Shape:** A long string separated into three distinct segments by periods (`.`), representing `header.payload.signature` encoded in Base64URL.
* **Postman Header Syntax:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJle...

```



