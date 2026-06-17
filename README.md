# Django & DRF Banking API — Learning Project

A hands-on project covering Django views, Django REST Framework (DRF) patterns, and a full CRUD banking API with custom business logic. Built across six progressive tasks — from Django's built-in class-based views all the way to a production-ready REST API with Postman tests.

---

## Project Structure

```
DjangoViewCRUD/
├──config/
├──djangoViews/             # django-view, template, etc
├──drfViews/                # APIView, GenericView, ModelViewSet
├── crudApi/
│   ├── models.py           # Account + Transaction models
│   ├── serializers.py      # List + Detail serializers for each model
│   ├── views.py            # AccountViewSet + TransactionViewSet
│   ├── permissions.py      # IsAccountOwner custom permission
│   └── urls.py             # DefaultRouter wiring
├── docs/
│   ├── drf_views_comparison.md        # Task 1 deliverable
│   ├── crudApi.md               # Tasks 2–4 deliverable
│   ├── apiDesignDoc.md              # Task 5 design document
│   └── bankingApiCollection.json
└── README.md
```

---

## Task Overview

| Task | Topic | Deliverable |
|------|-------|-------------|
| Task 0 | Django class-based views | `django_views_comparison.py` |
| Task 1 | DRF view styles comparison | `drf_views_comparison.md` |
| Task 2 | Full CRUD with ModelViewSet + Router | `full_crud_api.md` |
| Task 3 | Custom `@action` methods | Part of `full_crud_api.md` |
| Task 4 | `get_queryset` + `get_serializer_class` overrides | Part of `full_crud_api.md` |
| Task 5 | API design doc + Postman collection | `api_design_doc.md` + `.json` |

---

## Task 0 — Django Class-Based Views

**Goal:** Understand Django's built-in view classes before touching DRF.

Implemented the same set of Account-related pages using six different Django view classes, each at a different level of abstraction.

### Views Covered

| Class | Use Case |
|-------|----------|
| `View` | Base class — full manual control over HTTP methods |
| `TemplateView` | Render a template with context, no model needed |
| `ListView` | Display a list of model objects with pagination |
| `CreateView` | Handle a ModelForm to create a new object |
| `UpdateView` | Handle a ModelForm to edit an existing object |
| `DeleteView` | Confirm and delete an object, redirect after |

### Key Concepts Learned

- Every Django CBV maps HTTP methods (`get`, `post`) to class methods of the same name.
- `ListView` and `DetailView` auto-generate the template name from the model name (`account_list.html`, `account_detail.html`).
- `CreateView` and `UpdateView` handle form validation and re-rendering on error automatically — you only need to define `model`, `fields`, and `success_url`.
- `get_queryset()` is the correct override point for filtering (e.g. show only the current user's objects).

### When to Use Each

```
View          → Full control, non-model pages, custom HTTP logic
TemplateView  → Static or context-only pages (landing page, about, dashboard shell)
ListView      → Read-only list of model records
CreateView    → New object form
UpdateView    → Edit existing object form
DeleteView    → Confirm-and-delete flow
```

---

## Task 1 — DRF Views Comparison

**Goal:** Understand the three levels of DRF views by implementing the same Account CRUD endpoint three different ways.

**Deliverable:** [`drf_views_comparison.md`](./docs/drf_views_comparison.md)

### Styles Compared

**Style 1 — `APIView`**
The lowest level. You write every `get()`, `post()`, `put()`, `patch()`, and `delete()` method yourself. No automatic pagination, no queryset handling. Best when the endpoint doesn't map cleanly to a single model (e.g. an analytics endpoint, a webhook handler, or a login view).

**Style 2 — `GenericAPIView` + Mixins**
Adds reusable mixin classes (`ListModelMixin`, `CreateModelMixin`, etc.) that handle the standard response patterns. You still define two classes (one for list/create, one for retrieve/update/destroy) and wire HTTP methods to mixin methods manually. Best when you need standard behavior for some actions but custom behavior for others.

**Style 3 — `ModelViewSet`**
A single class that provides all five CRUD actions out of the box. Pairs with `DefaultRouter` to auto-generate all URLs. Supports custom `@action` methods and clean overrides via `get_queryset()` and `get_serializer_class()`. This is the right default for 90% of REST endpoints.

### Quick Comparison

| Feature | `APIView` | `GenericAPIView` | `ModelViewSet` |
|---------|-----------|------------------|----------------|
| Boilerplate | High | Medium | Low |
| Router support | No | No | ✅ Yes |
| Mixin composition | No | ✅ Yes | Implicit |
| Auto pagination | No | ✅ Yes | ✅ Yes |
| Custom `@action` | Manual | Manual | ✅ Built-in |
| Best for full CRUD | ✗ | Possible | ✅ Yes |
| Best for non-model views | ✅ Yes | Possible | ✗ |

---

## Task 2 — Full CRUD API (ModelViewSet + DefaultRouter)

**Goal:** Build a production-ready CRUD API for `Account` and `Transaction` using `ModelViewSet` wired to `DefaultRouter`.

**Deliverable:** [`full_crud_api.md`](./docs/full_crud_api.md)

### Models

**`Account`** — Belongs to a user, holds a balance, has a status (`active`, `frozen`, `closed`).

**`Transaction`** — Linked to an account, records `amount`, `transaction_type` (`deposit`, `withdrawal`, `transfer`), and snapshots `balance_before`/`balance_after`. Has a UUID `reference` field and a self-referencing `reversed_by` FK for reversals.

### Router Registration

```python
router = DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"transactions", TransactionViewSet, basename="transaction")
```

This auto-generates 11 URL patterns covering all CRUD actions plus custom actions.

### Auto-Generated Endpoints

```
GET    /api/accounts/                → list
POST   /api/accounts/                → create
GET    /api/accounts/{id}/           → retrieve
PUT    /api/accounts/{id}/           → update
PATCH  /api/accounts/{id}/           → partial_update
DELETE /api/accounts/{id}/           → destroy

GET    /api/transactions/            → list
POST   /api/transactions/            → create
GET    /api/transactions/{id}/       → retrieve
PATCH  /api/transactions/{id}/       → partial_update
DELETE /api/transactions/{id}/       → destroy
```

---

## Task 3 — Custom `@action` Methods

**Goal:** Extend the ViewSets with business-specific endpoints that go beyond standard CRUD.

**Deliverable:** Part of [`full_crud_api.md`](./docs/full_crud_api.md)

### Actions Implemented

#### `POST /accounts/{id}/freeze/`
Sets an active account's status to `frozen`. Returns 400 if already frozen or closed. Frozen accounts block new transactions.

#### `POST /accounts/{id}/unfreeze/`
Reactivates a frozen account back to `active`. Returns 400 if not currently frozen.

#### `GET /accounts/{id}/statement/`
Returns a transaction history with summary stats (total deposits, total withdrawals, transaction count). Supports `?from=` and `?to=` date filters.

#### `POST /transactions/{id}/reverse/`
Reverses a completed transaction by:
1. Creating an equal-and-opposite transaction (deposit ↔ withdrawal)
2. Updating the account balance atomically
3. Marking the original transaction as `reversed` and linking it to the new reversal record

Returns 400 if the transaction is already reversed or not in a `completed` state.

### How `@action` Works

```python
@action(detail=True, methods=["post"], url_path="freeze")
def freeze(self, request, pk=None):
    ...
```

- `detail=True` means the action requires a `{pk}` in the URL (object-level)
- `detail=False` would be collection-level (e.g. `/accounts/bulk-import/`)
- `url_path` sets the URL segment; defaults to the method name if omitted

---

## Task 4 — `get_queryset` and `get_serializer_class` Overrides

**Goal:** Scope data to the logged-in user and use different serializers depending on the action.

**Deliverable:** Part of [`full_crud_api.md`](./docs/full_crud_api.md)

### `get_queryset` — Per-User Filtering

Both `AccountViewSet` and `TransactionViewSet` override `get_queryset` to filter by the authenticated user. This prevents horizontal privilege escalation — a user requesting `/accounts/99/` where account 99 belongs to someone else gets a 404, not a 403, which avoids leaking the existence of the resource.

```python
def get_queryset(self):
    return Account.objects.filter(owner=self.request.user)
```

Both viewsets also support optional query-string filters (`?type=`, `?status=`, `?account=`) applied on top of the user filter.

### `get_serializer_class` — Action-Aware Serializers

List endpoints return a lightweight serializer (fewer fields, faster queries). Retrieve/create/update endpoints return a full serializer with all fields including computed ones like `transaction_count`.

```python
def get_serializer_class(self):
    if self.action == "list":
        return AccountListSerializer   # minimal — id, number, balance, status
    return AccountDetailSerializer     # full — all fields + transaction_count
```

This pattern avoids over-fetching on list pages and ensures detail pages have everything they need.

---

## Task 5 — API Design Document + Postman Collection

**Goal:** Document the API formally and verify every endpoint with automated Postman tests.

### Deliverables

**[`api_design_doc.md`](./docs/api_design_doc.md)**
Covers every endpoint with HTTP method, URL, request body shape, response shape (success and error), field-level notes, and a bugs-found table.

**[`banking_api.postman_collection.json`](./docs/banking_api.postman_collection.json)**
Import into Postman. The collection includes:
- Auth flow with automatic JWT token extraction into a `{{token}}` collection variable
- Happy-path tests for every endpoint with `pm.test()` assertions
- Edge-case and negative tests: insufficient balance, frozen account, already-reversed transaction, cross-user access, unauthenticated requests

### Bugs Found During Testing

| # | Endpoint | Issue | Severity |
|---|----------|-------|----------|
| 1 | `POST /transactions/` | Balance and transaction could desync if DB write fails mid-way — fixed with `@db_transaction.atomic` | High |
| 2 | `GET /accounts/{id}/statement/` | Passing `?from=abc` causes an unhandled `ValueError` — needs try/except with 400 response | Medium |
| 3 | `DELETE /transactions/{id}/` | Deleting a completed transaction doesn't reverse its balance effect | Medium |
| 4 | `POST /accounts/` | `account_number` uniqueness DB error not caught — resolved by `UniqueValidator` on serializer | Low |
| 5 | `POST /transactions/{id}/reverse/` | Race condition — two concurrent requests can both pass the status check before either updates; fix with `select_for_update()` | High |

---

## Setup

```bash
pip install django djangorestframework djangorestframework-simplejwt

# settings.py
INSTALLED_APPS = ["rest_framework", "banking"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

python manage.py makemigrations banking
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Stack

- Python 3.11+
- Django 5.x
- Django REST Framework 3.15+
- `djangorestframework-simplejwt` for JWT auth
- Postman for endpoint testing