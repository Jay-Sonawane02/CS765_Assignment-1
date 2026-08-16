"""
Network latency and message passing logic
"""
import random


class NetworkLink:
    def __init__(self, node_a: int, node_b: int, is_fast_a: bool, is_fast_b: bool):
        self.node_a = node_a
        self.node_b = node_b
        # Propagation delay: uniform [10ms, 500ms] in seconds
        self.rho = random.uniform(0.01, 0.5)
        # Link speed: 100 Mbps if both fast, else 5 Mbps
        self.c = 100_000_000 if is_fast_a and is_fast_b else 5_000_000

    def latency(self, message_bits: int) -> float:
        # Queuing delay: exponential with mean 96kbits/cij
        mean_queue_delay = 96_000 / self.c
        d = random.expovariate(1.0 / mean_queue_delay)
        # Total latency: rho + transmission + queuing
        transmission = message_bits / self.c
        return self.rho + transmission + d

def get_message_size(message_type: str, num_txns: int = 1) -> int:
    """
    Returns message size in bits.
    Transaction: 1 KB = 8192 bits
    Block: coinbase + txns, max 1 MB (8,388,608 bits)
    """
    if message_type == "txn":
        return 8192
    elif message_type == "block":
        # 1 KB coinbase + 1 KB per txn, max 1 MB
        size = 8192 + num_txns * 8192
        return min(size, 8_388_608)
    return 0
