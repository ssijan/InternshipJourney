# ORM Query Output Report

This document contains the output generated from the ORM queries implemented for the Fintech System project.

---

## Query 1 - All Accounts

**Purpose:** Retrieve all accounts from the database.

### Output

```text
Account: ACC1001 | Balance: 50500.00
Account: ACC1002 | Balance: 120500.00
```

---

## Query 2 - Balance Greater Than 10000

**Purpose:** Filter accounts with balance greater than 10,000.

### Output

```text
ACC1001
ACC1002
```

---

## Query 3 - Large Transactions

**Purpose:** Retrieve transactions with amount greater than 5,000.

### Output

```text
3 10000.00
4 15000.00
```

---

## Query 4 - Q Objects

**Purpose:** Demonstrate complex filtering using Q objects.

### Output

```text
3 DEBIT 10000.00
4 CREDIT 15000.00
```

---

## Query 5 - F Expression

**Purpose:** Update balances using database-side arithmetic.

### Output

```text
Added 100 to all account balances.
```

---

## Query 6 - Count Transactions

**Purpose:** Count total transactions for each account.

### Output

```text
ACC1001 2
ACC1002 2
```

---

## Query 7 - Total Transaction Amount

**Purpose:** Calculate total transaction amount.

### Output

```text
{'total_amount': Decimal('28000')}
```

---

## Query 8 - Average Transaction Amount

**Purpose:** Calculate average transaction amount.

### Output

```text
{'average_amount': Decimal('7000')}
```

---

## Query 9 - Maximum Transaction Amount

**Purpose:** Find the highest transaction amount.

### Output

```text
{'max_amount': Decimal('15000')}
```

---

## Query 10 - Minimum Transaction Amount

**Purpose:** Find the smallest transaction amount.

### Output

```text
{'min_amount': Decimal('500')}
```

---

## Query 11 - Merchant Transaction Count

**Purpose:** Count transactions per merchant.

### Output

```text
Amazon 2
Starbucks 1
```

---

## Query 12 - Case / When Conditional Expression

**Purpose:** Categorize transactions based on amount.

### Output

```text
2500.00 Normal
500.00 Normal
10000.00 Normal
15000.00 Large
```

---

## Query 13 - select_related()

**Purpose:** Reduce N+1 queries by joining ForeignKey relationships in a single SQL query.

### Output

```text
ACC1001 Amazon
ACC1001 Starbucks
ACC1002 Amazon
ACC1002 No Merchant
```

### Optimization

Without `select_related()`:

```python
for transaction in Transaction.objects.all():
    print(transaction.account.account_number)
```

This would trigger additional database queries for each related account.

Using:

```python
Transaction.objects.select_related(
    "account",
    "merchant"
)
```

loads related objects in a single query and eliminates the N+1 problem.

---

## Query 14 - prefetch_related()

**Purpose:** Optimize reverse ForeignKey and OneToMany relationships.

### Output

```text
ACC1001
Transactions: 2
Cards: 1

ACC1002
Transactions: 2
Cards: 1
```

### Optimization

Using:

```python
Account.objects.prefetch_related(
    "transactions",
    "cards"
)
```

reduces the number of database queries by fetching related objects in advance.

---

## Query 15 - Subquery

**Purpose:** Retrieve each account along with its latest transaction amount using a subquery.

### Output

```text
ACC1001 500
ACC1002 15000
```

---

## Query 16 - Cards Expiring Within 2 Years

**Purpose:** Find cards that will expire within the next two years.

### Output

```text
Total cards: 2
No cards expiring within 2 years.
```

### Observation

The current dataset contains cards with expiry dates beyond the next two years, so no records were returned.

---

# Summary

### Concepts Covered

* Basic Filtering
* Foreign Key Relationships
* Q Objects
* F Expressions
* Aggregations
* Annotations
* Case / When Expressions
* Subqueries
* select_related()
* prefetch_related()
* N+1 Query Optimization

### Dataset Statistics

| Metric                     | Value  |
| -------------------------- | ------ |
| Total Accounts             | 2      |
| Total Cards                | 2      |
| Total Merchants            | 2      |
| Total Transactions         | 4      |
| Highest Transaction        | 15,000 |
| Lowest Transaction         | 500    |
| Total Transaction Amount   | 28,000 |
| Average Transaction Amount | 7,000  |
