# Blockchain-Based P2P Network Simulator

A comprehensive discrete-event simulator for a peer-to-peer (P2P) cryptocurrency network, modeling Bitcoin-like blockchain behavior. This simulator implements core blockchain mechanics including transaction generation, network topology, proof-of-work mining, block propagation, fork resolution, and network-wide consensus.

## Features

- **Event-Driven Architecture:** Priority queue for chronological event processing (transaction generation, block mining, message passing, etc.)
- **Configurable Network Topology:** Randomly connected peer network with connectivity validation
- **Node Classification:** Fast/slow nodes, high/low CPU nodes, customizable via command line
- **Transaction System:** Random transaction generation, exponential inter-arrival times, balance validation
- **Network Latency Simulation:** Realistic delays based on propagation, bandwidth, and queuing
- **Loop-less Message Forwarding:** Efficient transaction/block propagation without duplicates
- **Proof-of-Work Mining:** Simulated mining competition, hash power distribution, block validation
- **Fork Resolution:** Longest chain rule, orphan block handling, automatic chain reorganization
- **Data Logging:** Per-node logs for blockchain, block arrivals, mining events, transaction propagation, and network topology (JSON/CSV)
- **Advanced Modeling:** Block propagation delays, mining pool scenarios, selfish mining, network partitions, and performance optimizations

## How to Use

### Prerequisites
- Python 3.8+

### Installation
Clone the repository:
```bash
git clone https://github.com/harsh-official/Blockchain-Based-P2P-Network-Simulator.git
cd Blockchain-Based-P2P-Network-Simulator
```

### Running the Simulator
Run the main simulation script with configurable parameters:
```bash
python src/main.py \
  --nodes N \
  --slow-percent Z0 \
  --low-cpu-percent Z1 \
  --tx-rate TTX \
  --block-interval I \
  --simulation-time T \
  --output-dir DIR
```

#### Example
```bash
python src/main.py --nodes 50 --slow-percent 20 --low-cpu-percent 30 --tx-rate 2.0 --block-interval 600 --simulation-time 3600 --output-dir logs
```

### Parameters
- `--nodes N`              Number of network nodes
- `--slow-percent Z0`      Percentage of slow nodes
- `--low-cpu-percent Z1`   Percentage of low CPU nodes
- `--tx-rate TTX`          Mean transaction inter-arrival time (seconds)
- `--block-interval I`     Target block generation interval (seconds)
- `--simulation-time T`    Total simulation duration (seconds)
- `--output-dir DIR`       Output directory for logs

### Output
Simulation logs and analysis files are saved in the specified output directory, including:
- Blockchain tree per node
- Block arrival timestamps
- Mining events and durations
- Transaction propagation logs
- Network topology connections
- Hash power distribution records

## License
MIT

