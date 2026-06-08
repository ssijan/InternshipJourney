# Full CRUD API — Account & Transaction

# Banking API

A RESTful Banking API built with Django REST Framework using `ModelViewSet` and `DefaultRouter`.

## Features

* Full CRUD for Accounts and Transactions
* User-specific data access
* Account freeze/unfreeze functionality
* Account statement generation
* Transaction reversal support
* Atomic balance updates
* Object-level permissions
* Action-based serializers

## Models

### Account

* Owner
* Account Number
* Account Type
* Balance
* Status (Active/Frozen/Closed)

### Transaction

* UUID Reference
* Transaction Type
* Amount
* Balance Snapshots
* Status
* Reversal Tracking

## Security

* Authentication required
* Users can access only their own accounts and transactions
* Owner is assigned automatically from `request.user`

## Custom Endpoints

### Account

* `POST /accounts/{id}/freeze/`
* `POST /accounts/{id}/unfreeze/`
* `GET /accounts/{id}/statement/`

### Transaction

* `POST /transactions/{id}/reverse/`

## Key Design Patterns

* `get_queryset()` for per-user filtering
* `get_serializer_class()` for action-based serializers
* `@transaction.atomic` for balance consistency
* Custom permissions for ownership validation

## Result

The API provides secure account management, transaction processing, audit-friendly transaction history, and reliable balance handling following common banking system practices.


### All Generated URLs

```
GET    /api/accounts/                    → list
POST   /api/accounts/                    → create
GET    /api/accounts/{id}/               → retrieve
PUT    /api/accounts/{id}/               → update
PATCH  /api/accounts/{id}/               → partial_update
DELETE /api/accounts/{id}/               → destroy
POST   /api/accounts/{id}/freeze/        → freeze  (custom)
POST   /api/accounts/{id}/unfreeze/      → unfreeze (custom)
GET    /api/accounts/{id}/statement/     → statement (custom)

GET    /api/transactions/                → list
POST   /api/transactions/                → create
GET    /api/transactions/{id}/           → retrieve
PATCH  /api/transactions/{id}/           → partial_update
DELETE /api/transactions/{id}/           → destroy
POST   /api/transactions/{id}/reverse/   → reverse (custom)
```

---