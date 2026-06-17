# Fintech ORM & Query Optimization Project

## Objective

This project demonstrates advanced Django ORM concepts including:

* select_related()
* prefetch_related()
* F Expressions
* Q Objects
* annotate()
* aggregate()
* Subquery
* Conditional Expressions

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## Project Structure

```text
django_orm/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── fintech/
│   ├── models.py
│   ├── managers.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── manage.py
├── orm_queries.py
├── seed_data.py
├── ORM_QUERY_REPORT.md
├── requirements.txt
└── README.md
```

---

## Database Schema

### User

Represents the application user.

### Account

Stores account information.

### Card

Stores debit/credit card information.

### Merchant

Stores merchant details.

### Transaction

Stores financial transactions.

---

## Running The Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run server:

```bash
python manage.py runserver
```

---

## Generate Sample Data

```bash
python manage.py shell
```

```python
from fintech.seed_data import seed_data

seed_data()
```

---

## Run ORM Queries

```python
from fintech.orm_queries import run_all_queries

run_all_queries()
```

---

## API Endpoints

### Accounts

```text
GET     /api/accounts/
GET     /api/accounts/<id>/
POST    /api/accounts/
PATCH   /api/accounts/<id>/
DELETE  /api/accounts/<id>/
```

### Transactions

```text
GET     /api/transactions/
GET     /api/transactions/<id>/
POST    /api/transactions/
PATCH   /api/transactions/<id>/
DELETE  /api/transactions/<id>/
```

### Merchants

```text
GET     /api/merchants/
GET     /api/merchants/<id>/
POST    /api/merchants/
PATCH   /api/merchants/<id>/
DELETE  /api/merchants/<id>/
```

### Cards

```text
GET     /api/cards/

```

---

## Learning Outcomes

* Advanced Django ORM
* Database Optimization
* Query Analysis
* API Development Using DRF
* Fintech Data Modeling

## Author
```text
Md. Sakibur Rahman (Sijan)

```