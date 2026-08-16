"""
Blockchain and block logic
"""
from typing import List, Dict

class Block:
    def __init__(self, block_id: str, prev_hash: str, transactions: List, coinbase_txn: str, timestamp: float):
        self.block_id = block_id
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.coinbase_txn = coinbase_txn
        self.timestamp = timestamp

class Blockchain:
    def __init__(self):
        self.blocks: Dict[str, Block] = {}
        self.genesis_block = None
        self.longest_chain = []

    def add_block(self, block: Block):
        # TODO: Add block and update longest chain
        pass
