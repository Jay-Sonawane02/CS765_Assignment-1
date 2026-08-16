"""
Node class and network topology logic
"""
import random
from typing import List, Dict


class Node:
    def __init__(self, node_id: int, is_slow: bool, is_low_cpu: bool, initial_balance: float):
        self.node_id = node_id  # Unique ID
        self.is_slow = is_slow  # True if slow, False if fast
        self.is_low_cpu = is_low_cpu  # True if low CPU, False if high CPU
        self.balance = initial_balance
        self.peers: List[int] = []  # Connected peer IDs
        self.blockchain = None  # To be initialized

    def connect_peer(self, peer_id: int):
        if peer_id not in self.peers:
            self.peers.append(peer_id)

class NetworkTopology:
    def __init__(self, num_nodes: int, min_degree: int = 3, max_degree: int = 6):
        self.num_nodes = num_nodes
        self.adj_list: Dict[int, List[int]] = {i: [] for i in range(num_nodes)}


    def generate(self):
        # Randomly connect each node to 3-6 peers
        for node in range(self.num_nodes):
            degree = random.randint(3, 6)
            while len(self.adj_list[node]) < degree:
                peer = random.randint(0, self.num_nodes - 1)
                if peer != node and peer not in self.adj_list[node]:
                    self.adj_list[node].append(peer)
                    self.adj_list[peer].append(node)
        # Ensure connectivity
        while not self.is_connected():
            # If not connected, clear and regenerate
            self.adj_list = {i: [] for i in range(self.num_nodes)}
            for node in range(self.num_nodes):
                degree = random.randint(3, 6)
                while len(self.adj_list[node]) < degree:
                    peer = random.randint(0, self.num_nodes - 1)
                    if peer != node and peer not in self.adj_list[node]:
                        self.adj_list[node].append(peer)
                        self.adj_list[peer].append(node)

    def is_connected(self) -> bool:
        # BFS connectivity check
        visited = set()
        queue = [0]
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                queue.extend([peer for peer in self.adj_list[node] if peer not in visited])
        return len(visited) == self.num_nodes
