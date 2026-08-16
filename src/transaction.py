"""
Transaction logic
"""
import uuid
import random



class Transaction:
    def __init__(self, sender_id: int, receiver_id: int, amount: float):
        self.txn_id = str(uuid.uuid4())  # Unique transaction ID
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.size_kb = 1  # Transaction size is 1 KB

    def __str__(self):
        return f"{self.txn_id}: {self.sender_id} pays {self.receiver_id} {self.amount} coins"

    def is_valid(self, sender_balance: float) -> bool:
        # Ensure amount is less than or equal to sender's balance
        return self.amount <= sender_balance

    def to_dict(self):
        return {
            "txn_id": self.txn_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "amount": self.amount,
            "size_kb": self.size_kb
        }
