import os
import json
import pandas as pd
import matplotlib.pyplot as plt

LOG_DIR = "logs"

# 1. Blocks mined per node
block_files = [f for f in os.listdir(LOG_DIR) if f.startswith("block_") and f.endswith(".json")]
miners = []
for fname in block_files:
    with open(os.path.join(LOG_DIR, fname)) as f:
        data = json.load(f)
        miners.append(data["miner"])
if miners:
    miner_counts = pd.Series(miners).value_counts().sort_index()
    plt.figure()
    miner_counts.plot(kind="bar")
    plt.title("Blocks Mined per Node")
    plt.xlabel("Node ID")
    plt.ylabel("Blocks Mined")
    plt.tight_layout()
    plt.savefig("blocks_mined_per_node.png")
    print("Saved: blocks_mined_per_node.png")
else:
    print("No block data found. No blocks mined or logs missing.")

# 2. Transaction amount distribution
txn_files = [f for f in os.listdir(LOG_DIR) if f.startswith("txn_") and f.endswith(".json")]
txn_amounts = []
for fname in txn_files:
    with open(os.path.join(LOG_DIR, fname)) as f:
        data = json.load(f)
        txn_amounts.append(data["amount"])
if txn_amounts:
    plt.figure()
    pd.Series(txn_amounts).plot(kind="hist", bins=20)
    plt.title("Transaction Amount Distribution")
    plt.xlabel("Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("transaction_amount_distribution.png")
    print("Saved: transaction_amount_distribution.png")
else:
    print("No transaction data found.")

# 3. Longest chain length per node
chain_files = [f for f in os.listdir(LOG_DIR) if f.startswith("blockchain_tree_") and f.endswith(".json")]
chain_lengths = {}
for fname in chain_files:
    with open(os.path.join(LOG_DIR, fname)) as f:
        data = json.load(f)
        chain_lengths[data["node_id"]] = len(data["longest_chain"])
if chain_lengths:
    plt.figure()
    pd.Series(chain_lengths).sort_index().plot(kind="bar")
    plt.title("Longest Chain Length per Node")
    plt.xlabel("Node ID")
    plt.ylabel("Chain Length")
    plt.tight_layout()
    plt.savefig("longest_chain_length_per_node.png")
    print("Saved: longest_chain_length_per_node.png")
else:
    print("No blockchain tree data found.")

print("Visualization complete.")
