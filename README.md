Splitwise-like Expense Sharing Application
This is a Django-based application that allows users to manage shared expenses and track balances between users. It includes endpoints for creating users, expenses, expense participants, and balance entries.

Table of Contents
  Installation
  Running the Application
  API Endpoints
  Create a User
  Create an Expense
  Create an ExpenseParticipant
  Create a Balance Entry
  Testing the API

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/erpawan/Splitwise.git
cd Splitwise
Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Apply migrations:

python manage.py migrate
Create a superuser (optional):

python manage.py createsuperuser
Running the Application
Start the development server:

python manage.py runserver
The application will be available at http://127.0.0.1:8000/.

API Endpoints
1. Create a User
Endpoint: POST /api/users/

Request Body:

json
Copy code
{
  "username": "john_doe",
  "password": "password123",
  "email": "john.doe@example.com",
  "mobile_number": "1234567890"
}
2. Create an Expense
Endpoint: POST /api/expenses/

Request Body:

json
Copy code
{
  "description": "Lunch at café",
  "amount": "1500.00",
  "split_type": "EQUAL",
  "created_by": 1,
  "participants": [
    {"user": 2, "exact_amount": null, "percent": null}
  ]
}
3. Create an ExpenseParticipant
Endpoint: POST /api/expense-participants/

Request Body:

json
Copy code
{
  "user": 2,
  "expense": 1,
  "amount_owed": "1500.00",
  "exact_amount": null,
  "percent": null
}
4. Create a Balance Entry
Endpoint: POST /api/balance/

Request Body:

json
Copy code
{
  "lender": 1,
  "borrower": 2,
  "amount": "1500.00"
}
Testing the API
You can test the API using tools like Postman or cURL. Here are some example cURL commands:

1. Create a User
curl -X POST http://127.0.0.1:8000/api/users/ \
-H "Content-Type: application/json" \
-d '{"username": "john_doe", "password": "password123", "email": "john.doe@example.com", "mobile_number": "1234567890"}'

2. Create an Expense
curl -X POST http://127.0.0.1:8000/api/expenses/ \
-H "Content-Type: application/json" \
-d '{"description": "Lunch at café", "amount": "1500.00", "split_type": "EQUAL", "created_by": 1, "participants": [{"user": 2, "exact_amount": null, "percent": null}]}'

3. Create an ExpenseParticipant
curl -X POST http://127.0.0.1:8000/api/expense-participants/ \
-H "Content-Type: application/json" \
-d '{"user": 2, "expense": 1, "amount_owed": "1500.00", "exact_amount": null, "percent": null}'

4. Create a Balance Entry
curl -X POST http://127.0.0.1:8000/api/balance/ \
-H "Content-Type: application/json" \
-d '{"lender": 1, "borrower": 2, "amount": "1500.00"}'
