# Banking API — Design Document

**Version:** 1.0  
**Base URL:** `https://api.banking.local/api/`  
**Auth:** JWT Bearer Token (`Authorization: Bearer <token>`)  
**Content-Type:** `application/json`

---

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/token/` | Obtain JWT access + refresh tokens |
| POST | `/auth/token/refresh/` | Refresh access token |
| POST | `/auth/token/verify/` | Verify token validity |

### POST `/auth/token/`
**Request**
```json
{ "username": "sijan", "password": "sijan123" }
```
**Response 200**
```json
{
  "access":  "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>"
}
```
**Response 401**
```json
{ "detail": "No active account found with the given credentials" }
```

---

## Accounts

All endpoints require authentication. Users can only access their own accounts.

| Method | Endpoint | Action | Description |
|--------|----------|--------|-------------|
| GET | `/accounts/` | list | List all accounts for the logged-in user |
| POST | `/accounts/` | create | Open a new account |
| GET | `/accounts/{id}/` | retrieve | Get full account details |
| PUT | `/accounts/{id}/` | update | Full update of account |
| PATCH | `/accounts/{id}/` | partial_update | Partial update |
| DELETE | `/accounts/{id}/` | destroy | Close/delete account |
| POST | `/accounts/{id}/freeze/` | freeze | Freeze an active account |
| POST | `/accounts/{id}/unfreeze/` | unfreeze | Reactivate a frozen account |
| GET | `/accounts/{id}/statement/` | statement | Get transaction statement with summary |

---

### GET `/accounts/`
**Query Params**

| Param | Type | Description |
|-------|------|-------------|
| `type` | string | Filter by `savings`, `checking`, or `business` |
| `status` | string | Filter by `active`, `frozen`, or `closed` |

**Response 200**
```json
[
  {
    "id": 1,
    "account_number": "1234567890",
    "account_type": "savings",
    "balance": "15000.00",
    "status": "active",
    "owner_username": "alice",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

---

### POST `/accounts/`
**Request Body**
```json
{
  "account_number": "9876543210",
  "account_type": "checking"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `account_number` | string | ✅ | Must be numeric, max 20 chars, unique |
| `account_type` | string | ✅ | `savings` / `checking` / `business` |

**Response 201**
```json
{
  "id": 2,
  "account_number": "9876543210",
  "account_type": "checking",
  "balance": "0.00",
  "status": "active",
  "owner": 1,
  "owner_username": "alice",
  "transaction_count": 0,
  "created_at": "2024-06-08T12:00:00Z",
  "updated_at": "2024-06-08T12:00:00Z"
}
```

**Response 400** (validation error)
```json
{
  "account_number": ["Account number must be numeric."],
  "account_type": ["\"premium\" is not a valid choice."]
}
```

---

### GET `/accounts/{id}/`
**Response 200**
```json
{
  "id": 1,
  "account_number": "1234567890",
  "account_type": "savings",
  "balance": "15000.00",
  "status": "active",
  "owner": 1,
  "owner_username": "alice",
  "transaction_count": 47,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-06-07T09:30:00Z"
}
```
**Response 404** — account not found or not owned by user

---

### POST `/accounts/{id}/freeze/`
**Request Body:** `{}` (empty)

**Response 200**
```json
{ "detail": "Account frozen.", "status": "frozen" }
```

**Response 400** (already frozen)
```json
{ "detail": "Cannot freeze an account with status 'frozen'." }
```

---

### POST `/accounts/{id}/unfreeze/`
**Request Body:** `{}` (empty)

**Response 200**
```json
{ "detail": "Account reactivated.", "status": "active" }
```

---

### GET `/accounts/{id}/statement/`
**Query Params**

| Param | Type | Example | Description |
|-------|------|---------|-------------|
| `from` | date | `2024-01-01` | Start date (inclusive) |
| `to` | date | `2024-06-30` | End date (inclusive) |

**Response 200**
```json
{
  "account": {
    "id": 1,
    "account_number": "1234567890",
    "balance": "15000.00",
    "status": "active"
  },
  "period": { "from": "2024-01-01", "to": "2024-06-30" },
  "summary": {
    "total_deposits": "25000.00",
    "total_withdrawals": "10000.00",
    "transaction_count": 12
  },
  "transactions": [
    {
      "reference": "550e8400-e29b-41d4-a716-446655440000",
      "transaction_type": "deposit",
      "amount": "5000.00",
      "balance_before": "10000.00",
      "balance_after": "15000.00",
      "description": "Monthly salary",
      "status": "completed",
      "created_at": "2024-06-01T09:00:00Z"
    }
  ]
}
```

---

## Transactions

Users can only access transactions belonging to their own accounts.

| Method | Endpoint | Action | Description |
|--------|----------|--------|-------------|
| GET | `/transactions/` | list | List user's transactions |
| POST | `/transactions/` | create | Create a new transaction |
| GET | `/transactions/{id}/` | retrieve | Full transaction detail |
| PATCH | `/transactions/{id}/` | partial_update | Update description only |
| DELETE | `/transactions/{id}/` | destroy | Delete transaction record |
| POST | `/transactions/{id}/reverse/` | reverse | Reverse a completed transaction |

---

### GET `/transactions/`
**Query Params**

| Param | Type | Description |
|-------|------|-------------|
| `account` | integer | Filter by account ID |
| `type` | string | `deposit` / `withdrawal` / `transfer` |
| `status` | string | `pending` / `completed` / `reversed` / `failed` |

**Response 200**
```json
[
  {
    "id": 10,
    "reference": "550e8400-e29b-41d4-a716-446655440000",
    "transaction_type": "deposit",
    "amount": "5000.00",
    "status": "completed",
    "created_at": "2024-06-01T09:00:00Z"
  }
]
```

---

### POST `/transactions/`
**Request Body**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `account` | integer | ✅ | Must be owned by the requesting user |
| `transaction_type` | string | ✅ | `deposit` / `withdrawal` / `transfer` |
| `amount` | decimal | ✅ | Must be > 0 |
| `description` | string | ❌ | Optional memo |

```json
{
  "account": 1,
  "transaction_type": "deposit",
  "amount": "1000.00",
  "description": "Client payment"
}
```

**Response 201**
```json
{
  "id": 11,
  "reference": "7f000001-e29b-41d4-a716-446655441111",
  "account": 1,
  "transaction_type": "deposit",
  "amount": "1000.00",
  "balance_before": "14000.00",
  "balance_after": "15000.00",
  "description": "Client payment",
  "status": "completed",
  "reversed_by": null,
  "reversed_by_reference": null,
  "created_at": "2024-06-08T12:30:00Z"
}
```

**Response 400** — validation errors
```json
{
  "amount": ["Insufficient balance."],
  "account": ["Account is frozen and cannot accept transactions."]
}
```

---

### POST `/transactions/{id}/reverse/`
**Request Body**
```json
{ "reason": "Customer dispute — duplicate charge" }
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `reason` | string | ❌ | Defaults to "Manual reversal" |

**Response 200**
```json
{
  "detail": "Transaction reversed.",
  "original": {
    "id": 10,
    "reference": "550e8400-...",
    "status": "reversed",
    "amount": "5000.00",
    "transaction_type": "deposit"
  },
  "reversal": {
    "id": 12,
    "reference": "aabbccdd-...",
    "status": "completed",
    "amount": "5000.00",
    "transaction_type": "withdrawal",
    "description": "Reversal of 550e8400-.... Reason: Customer dispute — duplicate charge"
  }
}
```

**Response 400** (already reversed)
```json
{ "detail": "This transaction has already been reversed." }
```

---

## Error Response Shapes

| HTTP Code | Meaning | Shape |
|-----------|---------|-------|
| 400 | Bad Request / Validation | `{ "field": ["message"] }` or `{ "detail": "msg" }` |
| 401 | Unauthenticated | `{ "detail": "Authentication credentials were not provided." }` |
| 403 | Forbidden (wrong owner) | `{ "detail": "You do not have permission to perform this action." }` |
| 404 | Not Found | `{ "detail": "Not found." }` |
| 405 | Method Not Allowed | `{ "detail": "Method \"PUT\" not allowed." }` |
| 500 | Server Error | `{ "detail": "Internal server error." }` |

---

## Bugs Found During Testing

| # | Endpoint | Bug | Severity | Status |
|---|----------|-----|----------|--------|
| 1 | `POST /transactions/` | Missing atomic transaction — balance and transaction could desync if DB write fails mid-way. **Fix:** wrap `perform_create` in `@db_transaction.atomic`. | High | ✅ Fixed |
| 2 | `GET /accounts/{id}/statement/` | No date format validation on `from`/`to` params — passing `"abc"` raises unhandled `ValueError`. **Fix:** wrap in try/except, return 400. | Medium | ⚠️ Open |
| 3 | `DELETE /transactions/{id}/` | Deleting a completed transaction doesn't reverse balance. Consider soft-delete or restrict DELETE to `pending` only. | Medium | ⚠️ Open |
| 4 | `POST /accounts/` | `account_number` uniqueness error returns a 500 if DB integrity error is not caught. DRF handles this via `UniqueValidator` on the serializer field. Confirm serializer has `validators=[UniqueValidator(...)]` or that the model-level error is caught. | Low | ✅ Fixed via serializer |
| 5 | `POST /transactions/{id}/reverse/` | Race condition: two concurrent reverse requests on the same transaction could both pass the `status == "completed"` check before either updates. **Fix:** use `select_for_update()` inside atomic block. | High | ⚠️ Open |

---

## Implementation Notes

- All `GET` list endpoints should be paginated in production. Add `DEFAULT_PAGINATION_CLASS` to DRF settings.
- Token expiry: access token = 5 min, refresh = 7 days (recommended).
- `balance` field is read-only — it is only modified via transaction creation and reversal, never via direct Account update.
- The `reverse` action uses a simplified same-account credit model. In a real system, transfers would involve two accounts and two transaction records atomically.