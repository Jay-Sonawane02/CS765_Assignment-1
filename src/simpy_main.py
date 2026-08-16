"""
SimPy-based discrete-event simulation for Blockchain-Based P2P Network Simulator
"""
import simpy
import random
from transaction import Transaction
from node import Node, NetworkTopology
from blockchain import Blockchain, Block
from logger import Logger

# Simulation parameters (can be replaced with argparse)
NODES = 10
SLOW_PERCENT = 20
LOW_CPU_PERCENT = 30
TX_RATE = 2.0
BLOCK_INTERVAL = 600
SIMULATION_TIME = 3600
OUTPUT_DIR = "logs"

class P2PSimulator:
    def __init__(self, env, num_nodes, tx_rate, block_interval):
        self.env = env
        self.tx_rate = tx_rate
        self.block_interval = block_interval
        self.logger = Logger(OUTPUT_DIR)
        self.nodes = []
        num_slow = int(num_nodes * SLOW_PERCENT / 100)
        num_low_cpu = int(num_nodes * LOW_CPU_PERCENT / 100)
        for i in range(num_nodes):
            is_slow = i < num_slow
            is_low_cpu = i < num_low_cpu
            node = Node(i, is_slow, is_low_cpu, initial_balance=1000)
            node.blockchain = Blockchain()
            self.nodes.append(node)
        self.topology = NetworkTopology(num_nodes)
        self.topology.generate()
        for node_id, peers in self.topology.adj_list.items():
            for peer_id in peers:
                self.nodes[node_id].connect_peer(peer_id)

    def run(self):
        for node in self.nodes:
            self.env.process(self.node_process(node))

    def node_process(self, node):
        while True:
            # Transaction generation
            yield self.env.timeout(random.expovariate(1.0 / self.tx_rate))
            receiver_id = random.choice([n.node_id for n in self.nodes if n.node_id != node.node_id])
            amount = random.uniform(1, 10)
            if node.balance >= amount:
                txn = Transaction(sender_id=node.node_id, receiver_id=receiver_id, amount=amount)
                node.balance -= amount
                self.nodes[receiver_id].balance += amount
                self.logger.log(f"txn_{txn.txn_id}.json", txn.to_dict())
                # Forward transaction to peers (simplified)
                for peer_id in node.peers:
                    pass # Add SimPy event for message passing if needed
            # Mining (simplified)
            yield self.env.timeout(random.expovariate(1.0 / self.block_interval))
            block_id = f"blk_{random.getrandbits(64)}"
            coinbase = f"{block_id}: {node.node_id} mines 50 coins"
            block = Block(block_id=block_id, prev_hash=node.blockchain.longest_chain[-1] if node.blockchain.longest_chain else "genesis", transactions=[], coinbase_txn=coinbase, timestamp=self.env.now)
            node.blockchain.blocks[block_id] = block
            node.blockchain.longest_chain.append(block_id)
            node.balance += 50
            self.logger.log(f"block_{block_id}.json", {
                "block_id": block_id,
                "miner": node.node_id,
                "coinbase": coinbase,
                "timestamp": self.env.now
            })

if __name__ == "__main__":
    env = simpy.Environment()
    sim = P2PSimulator(env, NODES, TX_RATE, BLOCK_INTERVAL)
    sim.run()
    env.run(until=SIMULATION_TIME)
    print(f"SimPy simulation completed. Logs saved to {OUTPUT_DIR}")
