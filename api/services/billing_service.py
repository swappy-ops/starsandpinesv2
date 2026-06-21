"""Billing service — business logic for ledger and payments.

Handles:
- Generate bill for a stay
- Record payment
- Calculate balance
"""

from api.repositories.ledger import LedgerRepository
from api.repositories.orders import OrderRepository


class BillingService:
    @staticmethod
    def get_bill(stay_id: str) -> dict:
        """Get complete bill for a stay: entries, balance, orders."""
        entries = LedgerRepository.get_by_stay(stay_id)
        balance = LedgerRepository.get_balance(stay_id)
        orders = OrderRepository.get_by_stay(stay_id)

        charges = [e for e in entries if e["amount"] > 0]
        payments = [e for e in entries if e["amount"] < 0]

        total_charges = sum(e["amount"] for e in charges)
        total_payments = sum(abs(e["amount"]) for e in payments)

        return {
            "stay_id": stay_id,
            "entries": entries,
            "orders": orders,
            "charges": charges,
            "payments": payments,
            "total_charges": total_charges,
            "total_payments": total_payments,
            "balance": balance,
        }

    @staticmethod
    def record_payment(stay_id: str, amount: float, method: str = "cash",
                       upi_txn_id: str = None, receipt_ref: str = None,
                       collected_by: str = None) -> dict:
        """Record a payment: adds to ledger and payments table."""
        import uuid
        from api.db import get_db
        from datetime import datetime

        # Add to ledger
        LedgerRepository.add_payment(
            stay_id=stay_id,
            description=f"Payment via {method}",
            amount=amount,
            created_by=collected_by,
        )

        # Add to payments table
        payment_id = f"pay_{uuid.uuid4().hex[:8]}"
        with get_db() as conn:
            conn.execute(
                "INSERT INTO payments (id, stay_id, amount, method, upi_txn_id, receipt_ref, collected_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (payment_id, stay_id, amount, method, upi_txn_id, receipt_ref, collected_by),
            )

        return {
            "payment_id": payment_id,
            "amount": amount,
            "method": method,
            "new_balance": LedgerRepository.get_balance(stay_id),
        }
