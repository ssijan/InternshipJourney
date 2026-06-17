# Fixed Serializer Test Cases

## Test Case 1: Invalid Account Number

### Problem

Account numbers shorter than 10 characters were accepted.

### Fix

Added field-level validation:

```python
def validate_account_number(self, value):
    if len(value) < 10:
        raise serializers.ValidationError(
            "Account number too short."
        )
    return value
```

---

## Test Case 2: Negative Transaction Amount

### Problem

Transactions allowed negative amounts.

### Fix

Added validation:

```python
def validate_amount(self, value):
    if value <= 0:
        raise serializers.ValidationError(
            "Amount must be greater than zero."
        )
    return value
```

---

## Test Case 3: Withdraw Exceeding Balance

### Problem

Users could withdraw more money than available.

### Fix

Added object-level validation:

```python
def validate(self, attrs):

    if (
        attrs["transaction_type"] == "withdraw"
        and attrs["amount"] > attrs["account"].balance
    ):
        raise serializers.ValidationError(
            "Insufficient balance."
        )

    return attrs
```

---

## Test Case 4: Writable Nested Serializer Failure

### Problem

Nested account and user creation raised:

```text
The .create() method does not support writable nested fields
```

### Fix

Implemented custom create():

```python
def create(self, validated_data):
    ...
```

---

## Test Case 5: Bulk Update Failure

### Problem

ListSerializer could create objects but failed during updates.

### Fix

Implemented custom update():

```python
def update(self, instances, validated_data):
    ...
```

and exposed the `id` field:

```python
id = serializers.IntegerField()
```

to map incoming data to existing objects.

---

## Result

All serializer tests now pass successfully and demonstrate:

* Field-level validation
* Object-level validation
* Nested writes
* Bulk create
* Bulk update
* Custom serializer fields
