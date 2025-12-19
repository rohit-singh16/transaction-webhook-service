📦 Transaction Webhook Service (Backend)

A production-ready backend service that receives transaction webhooks, responds immediately, and processes transactions reliably in the background with idempotency guarantees.

🔗 Live API (Deployed on Render):
https://transaction-webhook-service-lkeq.onrender.com

🧩 Problem Statement

This service is built as part of a Full Stack Engineer Assessment to simulate receiving transaction webhooks from external payment processors (e.g., Razorpay).

Key requirements covered:

Immediate webhook acknowledgment (≤ 500ms)

Background processing with artificial delay

Idempotent transaction handling

Persistent storage of transaction status

Publicly deployed API

🚀 API Endpoints
1️⃣ Health Check

GET /

Used to verify service availability.

Response

{
  "status": "HEALTHY",
  "current_time": "2024-01-15T10:30:00Z"
}
👉 Test it:
https://transaction-webhook-service-lkeq.onrender.com

2️⃣ Transaction Webhook

POST /v1/webhooks/transactions

Receives transaction events and immediately acknowledges them.

Request Body

{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}

Response

HTTP 202 Accepted

Response time: < 500ms

Processing happens asynchronously

👉 Test it:

POST https://transaction-webhook-service-lkeq.onrender.com/v1/webhooks/transactions
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_005",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 1500,
    "currency": "INR"
  }'

  3️⃣ Get Transaction Status

GET /v1/transactions/{transaction_id}

Used to verify background processing and idempotency.

Response

{
  "transaction_id": "txn_test_005",
  "source_account": "acc_user_1",
  "destination_account": "acc_merchant_1",
  "amount": 1500,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:30:30Z"
}

👉 Test it (after ~30 seconds):
https://transaction-webhook-service-lkeq.onrender.com/v1/transactions/txn_test_005

⚙️ How Background Processing Works

Webhook is acknowledged immediately (202 Accepted)

Transaction is queued for background execution

A 30-second delay simulates external service calls

Final transaction status is persisted

Duplicate webhooks with the same transaction_id are ignored (idempotency)

🔒 Idempotency Guarantee

transaction_id is treated as a unique key

Sending the same webhook multiple times:

Does NOT create duplicate records

Does NOT reprocess the transaction

This ensures safety against retries from payment providers

🧪 How You Can Verify-
✅ Scenario 1: Single Transaction

Send a webhook

Immediately receive 202 Accepted

Check status after 30 seconds → PROCESSED

✅ Scenario 2: Duplicate Prevention

Send the same webhook multiple times

Verify only one transaction is processed

✅ Scenario 3: Performance

Observe sub-500ms response for webhook endpoint

🛠️ Tech Stack

Backend: Python (FastAPI)

Async Processing: Background tasks

Database: Cloud-hosted persistent storage

Deployment: Render

API Design: RESTful

📸 Screenshot #1: Browser showing the healthy response
This service receives transaction webhooks, immediately acknowledges them, and processes them asynchronously in the background with idempotency support.
<img width="1326" height="457" alt="image" src="https://github.com/user-attachments/assets/7871b948-6759-4381-84e0-c221ca5a28a8" />

📸 Screenshot #2: Postman / curl response showing 202 Accepted
<img width="1272" height="763" alt="image" src="https://github.com/user-attachments/assets/22a1a098-40e5-45cf-9654-7020c651c415" />

Although the webhook responds immediately, the transaction is processed asynchronously in the background with a simulated delay.

📸 Screenshot #3: GET request showing status: PROCESSED
<img width="1342" height="859" alt="image" src="https://github.com/user-attachments/assets/c21d5562-81a1-4be1-b0a5-d11e547b9a32" />

📸 Screenshot #4: Duplicate Webhook - Duplicate webhook handled gracefully
<img width="1332" height="691" alt="image" src="https://github.com/user-attachments/assets/d173002d-ab03-4948-830b-4ad2c5dd2400" />
📸 Screenshot #4B — Verify Transaction State - No duplicate processing
<img width="1344" height="770" alt="image" src="https://github.com/user-attachments/assets/281ae2e4-367f-45de-b9fc-a0a27cd84185" />

Payment providers retry webhooks multiple times. Idempotency ensures duplicate payments are never processed.


<img width="1851" height="460" alt="image" src="https://github.com/user-attachments/assets/d60bc8e6-42f2-4588-b25e-d3d965244028" />







