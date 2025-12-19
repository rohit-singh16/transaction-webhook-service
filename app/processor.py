import time
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Transaction

def process_transaction(transaction_id: str, db: Session):
    # Simulate slow external API call
    time.sleep(30)

    txn = db.query(Transaction).filter(
        Transaction.transaction_id == transaction_id
    ).first()

    if not txn:
        return

    txn.status = "PROCESSED"
    txn.processed_at = datetime.utcnow()

    db.commit()
