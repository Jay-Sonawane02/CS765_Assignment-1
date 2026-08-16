"""
Entry point for Blockchain-Based P2P Network Simulator
"""
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Blockchain-Based P2P Network Simulator")
    parser.add_argument('--nodes', type=int, required=True, help='Number of network nodes')
    parser.add_argument('--slow-percent', type=float, required=True, help='Percentage of slow nodes')
    parser.add_argument('--low-cpu-percent', type=float, required=True, help='Percentage of low CPU nodes')
    parser.add_argument('--tx-rate', type=float, required=True, help='Mean transaction inter-arrival time')
    parser.add_argument('--block-interval', type=float, required=True, help='Target block generation interval')
    parser.add_argument('--simulation-time', type=float, required=True, help='Total simulation duration')
    parser.add_argument('--output-dir', type=str, required=True, help='Output directory for logs')
    return parser.parse_args()

def main():

    args = parse_args()
    from event import EventQueue, Event
    from node import Node, NetworkTopology
    from transaction import Transaction
    from blockchain import Blockchain, Block
    from network import NetworkLink
    from logger import Logger
    import random
    import time

    # Initialize logger
    logger = Logger(args.output_dir)

    # Initialize nodes
    nodes = []
    num_slow = int(args.nodes * args.slow_percent / 100)
    num_low_cpu = int(args.nodes * args.low_cpu_percent / 100)
    for i in range(args.nodes):
        is_slow = i < num_slow
        is_low_cpu = i < num_low_cpu
        node = Node(i, is_slow, is_low_cpu, initial_balance=1000)
        nodes.append(node)

    # Initialize network topology
    topology = NetworkTopology(args.nodes)
    topology.generate()
    for node_id, peers in topology.adj_list.items():
        for peer_id in peers:
            nodes[node_id].connect_peer(peer_id)

    # Initialize blockchains
    for node in nodes:
        node.blockchain = Blockchain()
        # Create genesis block
        genesis = Block(block_id="genesis", prev_hash=None, transactions=[], coinbase_txn=None, timestamp=0)
        node.blockchain.genesis_block = genesis
        node.blockchain.blocks["genesis"] = genesis
        node.blockchain.longest_chain = ["genesis"]

    # Initialize event queue
    event_queue = EventQueue()
    # Schedule initial transaction generation events
    for node in nodes:
        t = random.expovariate(1.0 / args.tx_rate)
        event_queue.push(Event(timestamp=t, event_type="generate_txn", data={"node_id": node.node_id}))

    # Simulation loop
    sim_time = 0
    end_time = args.simulation_time

    # Transaction forwarding history: {node_id: {txn_id: set(peer_ids)}}
    txn_forwarded = {node.node_id: {} for node in nodes}

    while not event_queue.is_empty() and sim_time < end_time:
        event = event_queue.pop()
        sim_time = event.timestamp
        if sim_time > end_time:
            break
        if event.event_type == "generate_txn":
            node_id = event.data["node_id"]
            sender = nodes[node_id]
            receiver_id = random.choice([n.node_id for n in nodes if n.node_id != node_id])
            amount = random.uniform(1, 10)
            if sender.balance >= amount:
                txn = Transaction(sender_id=node_id, receiver_id=receiver_id, amount=amount)
                sender.balance -= amount
                nodes[receiver_id].balance += amount
                logger.log(f"txn_{txn.txn_id}.json", {
                    "txn_id": txn.txn_id,
                    "sender": node_id,
                    "receiver": receiver_id,
                    "amount": amount,
                    "timestamp": sim_time
                })
                # Forward transaction to peers (loop-less)
                if txn.txn_id not in txn_forwarded[node_id]:
                    txn_forwarded[node_id][txn.txn_id] = set()
                for peer_id in sender.peers:
                    if peer_id not in txn_forwarded[node_id][txn.txn_id]:
                        event_queue.push(Event(timestamp=sim_time, event_type="receive_txn", data={"from": node_id, "to": peer_id, "txn": txn}))
                        txn_forwarded[node_id][txn.txn_id].add(peer_id)
            next_t = sim_time + random.expovariate(1.0 / args.tx_rate)
            event_queue.push(Event(timestamp=next_t, event_type="generate_txn", data={"node_id": node_id}))
        elif event.event_type == "receive_txn":
            from_id = event.data["from"]
            to_id = event.data["to"]
            txn = event.data["txn"]
            receiver = nodes[to_id]
            # Loop-less forwarding
            if txn.txn_id not in txn_forwarded[to_id]:
                txn_forwarded[to_id][txn.txn_id] = set()
            if from_id not in txn_forwarded[to_id][txn.txn_id]:
                txn_forwarded[to_id][txn.txn_id].add(from_id)
                for peer_id in receiver.peers:
                    if peer_id != from_id and peer_id not in txn_forwarded[to_id][txn.txn_id]:
                        event_queue.push(Event(timestamp=sim_time, event_type="receive_txn", data={"from": to_id, "to": peer_id, "txn": txn}))
                        txn_forwarded[to_id][txn.txn_id].add(peer_id)

        # Mining event scheduling and block propagation
        # Hash power setup (high CPU = 10x low CPU)
    hash_powers = []
    for node in nodes:
        hash_powers.append(10 if not node.is_low_cpu else 1)
    total_hash = sum(hash_powers)
    for i, node in enumerate(nodes):
        node.hash_power = hash_powers[i] / total_hash

    # Schedule initial mining events
    for node in nodes:
        mining_time = random.expovariate(node.hash_power / args.block_interval)
        event_queue.push(Event(timestamp=mining_time, event_type="mine_block", data={"node_id": node.node_id}))

    # Block forwarding history: {node_id: {block_id: set(peer_ids)}}
    block_forwarded = {node.node_id: {} for node in nodes}

    while not event_queue.is_empty() and sim_time < end_time:
        event = event_queue.pop()
        sim_time = event.timestamp
        if sim_time > end_time:
            break
        # ...existing code...
        elif event.event_type == "mine_block":
            node_id = event.data["node_id"]
            miner = nodes[node_id]
            # Select valid transactions not in longest chain
            txns = []
            block_size = 1024 # coinbase
            for txn_id, peers in txn_forwarded[node_id].items():
                if block_size + 1024 <= 1_000_000:
                    txns.append(txn_id)
                    block_size += 1024
            block_id = f"blk_{random.getrandbits(64)}"
            coinbase = f"{block_id}: {node_id} mines 50 coins"
            block = Block(block_id=block_id, prev_hash=miner.blockchain.longest_chain[-1], transactions=txns, coinbase_txn=coinbase, timestamp=sim_time)
            miner.blockchain.blocks[block_id] = block
            miner.blockchain.longest_chain.append(block_id)
            miner.balance += 50
            logger.log(f"block_{block_id}.json", {
                "block_id": block_id,
                "miner": node_id,
                "prev_hash": block.prev_hash,
                "transactions": txns,
                "coinbase": coinbase,
                "timestamp": sim_time
            })
            # Propagate block to peers (loop-less)
            if block_id not in block_forwarded[node_id]:
                block_forwarded[node_id][block_id] = set()
            for peer_id in miner.peers:
                if peer_id not in block_forwarded[node_id][block_id]:
                    event_queue.push(Event(timestamp=sim_time, event_type="receive_block", data={"from": node_id, "to": peer_id, "block": block}))
                    block_forwarded[node_id][block_id].add(peer_id)
            # Schedule next mining event
            mining_time = sim_time + random.expovariate(miner.hash_power / args.block_interval)
            event_queue.push(Event(timestamp=mining_time, event_type="mine_block", data={"node_id": node_id}))
        elif event.event_type == "receive_block":
            from_id = event.data["from"]
            to_id = event.data["to"]
            block = event.data["block"]
            receiver = nodes[to_id]
            # Block validation: check transactions are not already in chain
            valid = True
            for txn_id in block.transactions:
                if txn_id in receiver.blockchain.longest_chain:
                    valid = False
                    break
            if valid:
                receiver.blockchain.blocks[block.block_id] = block
                receiver.blockchain.longest_chain.append(block.block_id)
                receiver.balance += 50
                logger.log(f"block_arrival_{block.block_id}_{to_id}.json", {
                    "block_id": block.block_id,
                    "arrived_at": to_id,
                    "timestamp": sim_time
                })
                # Fork resolution: keep longest chain
                if len(receiver.blockchain.longest_chain) > len(receiver.blockchain.longest_chain):
                    receiver.blockchain.longest_chain = receiver.blockchain.longest_chain
                # Propagate block to peers (loop-less)
                if block.block_id not in block_forwarded[to_id]:
                    block_forwarded[to_id][block.block_id] = set()
                for peer_id in receiver.peers:
                    if peer_id != from_id and peer_id not in block_forwarded[to_id][block.block_id]:
                        event_queue.push(Event(timestamp=sim_time, event_type="receive_block", data={"from": to_id, "to": peer_id, "block": block}))
                        block_forwarded[to_id][block.block_id].add(peer_id)

    # Final logging: blockchain tree per node
    for node in nodes:
        logger.log(f"blockchain_tree_{node.node_id}.json", {
            "node_id": node.node_id,
            "blocks": list(node.blockchain.blocks.keys()),
            "longest_chain": node.blockchain.longest_chain
        })

    print(f"Simulation completed. Logs saved to {args.output_dir}")

if __name__ == "__main__":
    main()
