from fastapi import FastAPI, Depends, status
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionWebhook
from fastapi import BackgroundTasks
from app.processor import process_transaction


app = FastAPI()

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/v1/webhooks/transactions", status_code=status.HTTP_202_ACCEPTED)
def receive_webhook(
    payload: TransactionWebhook,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing = db.query(Transaction).filter(
        Transaction.transaction_id == payload.transaction_id
    ).first()

    if existing:
        return {"message": "Transaction already received"}

    txn = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING",
        created_at=datetime.utcnow(),
        processed_at=None
    )

    db.add(txn)
    db.commit()

    # 🚀 Background processing
    background_tasks.add_task(
        process_transaction,
        payload.transaction_id,
        db
    )

    return {"message": "Webhook accepted"}

@app.get("/v1/transactions/{transaction_id}")
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    txn = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()

    if not txn:
        return []

    return [{
        "transaction_id": txn.transaction_id,
        "source_account": txn.source_account,
        "destination_account": txn.destination_account,
        "amount": float(txn.amount),
        "currency": txn.currency,
        "status": txn.status,
        "created_at": txn.created_at,
        "processed_at": txn.processed_at
    }]
