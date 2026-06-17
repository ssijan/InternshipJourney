# Serializer Comparison Guide

## 1. Serializer

### What is it?

`Serializer` is the most basic serializer in Django REST Framework. Every field must be declared manually.

### Example

```python
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField()
    email = serializers.EmailField()
```

### When to Use

* Data does not come from a Django model
* Custom API responses
* External API integrations
* Learning serializer internals

### Pros

* Full control over fields
* Not tied to database models

### Cons

* More code
* Manual field definitions

---

## 2. ModelSerializer

### What is it?

`ModelSerializer` automatically generates serializer fields from a Django model.

### Example

```python
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
```

### When to Use

* Most CRUD APIs
* Model-based applications
* Standard DRF projects

### Pros

* Less code
* Automatic validation
* Easy maintenance

### Cons

* Less flexibility than Serializer

---

## 3. Flat Serializer

### What is it?

A serializer that returns only IDs for related objects.

### Example

```python
class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"
```

### Response

```json
{
    "id": 1,
    "account": 5,
    "amount": 500
}
```

### When to Use

* Large datasets
* Performance-sensitive APIs
* Mobile applications

### Pros

* Faster queries
* Smaller payloads

### Cons

* Requires additional API calls

---

## 4. Nested Serializer

### What is it?

A serializer that includes related object details instead of only IDs.

### Example

```python
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["id", "account_number"]


class TransactionSerializer(serializers.ModelSerializer):

    account = AccountSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"
```

### Response

```json
{
    "id": 1,
    "amount": 500,
    "account": {
        "id": 5,
        "account_number": "1234567890"
    }
}
```

### When to Use

* Detail views
* Rich API responses
* Dashboard applications

### Pros

* Fewer API requests
* Better developer experience

### Cons

* Larger payloads
* More database queries if not optimized

---

## 5. Writable Nested Serializer

### What is it?

Allows creating or updating related objects in a single request.

### Example

```python
{
    "amount": 500,
    "account": {
        "account_number": "1234567890",
        "user": {
            "full_name": "MD Sijan"
        }
    }
}
```

### Creates

```text
User
 ↓
Account
 ↓
Transaction
```

### When to Use

* Complex forms
* Multi-step object creation
* Banking, e-commerce, and CRM systems

### Pros

* One API request
* Better user experience

### Cons

* More complex serializer logic
* Requires custom create/update methods

---

## Which One Should I Choose?

| Scenario                        | Recommended Serializer     |
| ------------------------------- | -------------------------- |
| Non-model data                  | Serializer                 |
| Standard CRUD APIs              | ModelSerializer            |
| Large datasets                  | Flat Serializer            |
| Detailed API responses          | Nested Serializer          |
| Create related objects together | Writable Nested Serializer |

---

## Project Usage

This project demonstrates all major DRF serializer types:

* Serializer
* ModelSerializer
* ListSerializer
* Flat Serializer
* Nested Serializer
* Writable Nested Serializer
* Custom Fields
* SerializerMethodField
* Validation
* Bulk Operations
