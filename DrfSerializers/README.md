# DRF Serializers Deep Dive

A Django REST Framework project demonstrating advanced serializer concepts including custom fields, nested serializers, writable nested serializers, bulk operations with `ListSerializer`, field-level and object-level validation, and computed serializer fields.

## Features

### Serializer Types

* Serializer
* ModelSerializer
* ListSerializer
* Nested Serializer
* Writable Nested Serializer

### Custom Fields

* MoneyField

  * Stores values in USD
  * Displays values in BDT (Taka)

* MaskedCardField

  * Masks sensitive card information
  * Example: `1234567812345678` → `**** **** **** 5678`

### Validation

* Field-level validation
* Object-level validation

### Computed Fields

* SerializerMethodField
* Transaction count
* Last active timestamp
* Account balance display

### Serializer Customization

* `to_representation()`
* `to_internal_value()`

### Bulk Operations

* Bulk Create
* Bulk Update
* Custom ListSerializer

---

## Project Structure

```text
serializers/
│
├── fields.py
├── serializer.py
├── nested_serializer.py
└── bulk_serializer.py

views.py
urls.py
```

---

## Models

### User

```python
User
├── full_name
└── email
```

### Account

```python
Account
├── account_number
├── card_number
├── balance
└── is_active
```

### Transaction

```python
Transaction
├── account
├── amount
├── transaction_type
└── timestamp
```

---

## Custom Fields

### MoneyField

Converts currency automatically:

```text
Database (USD)
        ↓
MoneyField
        ↓
API Response (BDT)
```

Example:

```python
balance = MoneyField()
```

Response:

```json
{
    "balance": 12200
}
```

Stored in database:

```python
balance = 100
```

---

### MaskedCardField

Example:

Database:

```text
1234567812345678
```

API Response:

```text
**** **** **** 5678
```

---

## SerializerMethodField

Used for computed values.

### Transaction Count

```python
transaction_count = serializers.SerializerMethodField()
```

### Last Active

```python
last_active = serializers.SerializerMethodField()
```

---

## Validation

### Field-Level Validation

```python
def validate_account_number(self, value):
    if len(value) < 10:
        raise serializers.ValidationError(
            "Account number too short."
        )
    return value
```

### Object-Level Validation

```python
def validate(self, attrs):
    if not attrs.get("is_active") and attrs.get("balance", 0) > 0:
        raise serializers.ValidationError(
            "Cannot deactivate account with active balance."
        )
    return attrs
```

---

## Nested Serializer

Example Response

```json
{
    "id": 1,
    "amount": 500,
    "account": {
        "account_number": "1234567890",
        "user": {
            "full_name": "MD Sijan",
            "email": "sijan@example.com"
        }
    }
}
```

---

## Writable Nested Serializer

Create User, Account, and Transaction in a single request.

Example:

```json
{
    "amount": 500,
    "transaction_type": "deposit",
    "account": {
        "account_number": "1234567890",
        "user": {
            "full_name": "MD Sijan",
            "email": "sijan@example.com"
        }
    }
}
```

Creates:

```text
User
 ↓
Account
 ↓
Transaction
```

---

## Bulk Operations

### Bulk Create

Endpoint:

```http
POST /transactions/bulk_create/
```

Request:

```json
[
    {
        "account": 1,
        "amount": 100,
        "transaction_type": "deposit"
    },
    {
        "account": 1,
        "amount": 200,
        "transaction_type": "deposit"
    }
]
```

Uses:

```python
Transaction.objects.bulk_create()
```

---

### Bulk Update

Endpoint:

```http
PATCH /transactions/bulk_update/
```

Request:

```json
[
    {
        "id": 1,
        "amount": 500
    },
    {
        "id": 2,
        "amount": 900
    }
]
```

Uses custom `ListSerializer.update()` implementation.

---

## API Endpoints

### Users

```http
GET     /users/
POST    /users/

GET     /users/{id}/
PUT     /users/{id}/
PATCH   /users/{id}/
DELETE  /users/{id}/
```

### Accounts

```http
GET     /accounts/
POST    /accounts/

GET     /accounts/{id}/
PUT     /accounts/{id}/
PATCH   /accounts/{id}/
DELETE  /accounts/{id}/
```

### Transactions

```http
GET     /transactions/
POST    /transactions/

GET     /transactions/{id}/
PUT     /transactions/{id}/
PATCH   /transactions/{id}/
DELETE  /transactions/{id}/
```

### Bulk Endpoints

```http
POST    /transactions/bulk_create/
PATCH   /transactions/bulk_update/
```

---

## Concepts Demonstrated

* Serializer
* ModelSerializer
* ListSerializer
* Nested Serializer
* Writable Nested Serializer
* Custom Serializer Fields
* SerializerMethodField
* Field-Level Validation
* Object-Level Validation
* Bulk Create
* Bulk Update
* to_representation()
* to_internal_value()
* ModelViewSet
* Router-Based URLs

---

## Learning Outcomes

After completing this project, I gained hands-on experience with:

* Advanced Django REST Framework serializers
* Nested object creation and updates
* Custom serializer fields
* Serializer validation patterns
* Bulk operations with ListSerializer
* API design using ModelViewSet
* Data transformation using serializer hooks
* Real-world serializer architecture decisions

## Author

Md.Sakibur Rahman
```


