# Chat System Scaling Simulation

This project is a simple Python-based simulation to understand how chat systems behave under load.
It demonstrates the limitations of a single server and explores basic sharding strategies.
User-based, channel-based, and hash-based sharding are implemented and tested with simulated traffic.
The project highlights issues like load imbalance, hotspots, and system bottlenecks.
The simulation also includes stress testing scenarios and failure simulations to demonstrate data loss during shard outages.
The goal is to understand why systems fail under scale and load, not just how to build them.

## How to Run

1. Ensure you have Python 3 installed.
2. Run the simulation script from your terminal:
   ```bash
   python main.py
   ```
3. Observe the output detailing the 5 different simulation phases, from a naive single server to hash-based sharding with failure simulations.
