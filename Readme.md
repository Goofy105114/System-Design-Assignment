# Chat System Scaling Simulation

This project is a Python-based simulation designed to understand how chat systems scale and handle high load volumes.

It moves beyond basic setups to explore what happens when systems are pushed to their limits, demonstrating the strengths and weaknesses of common scaling patterns.

## Features Covered

1. **Single Server Bottlenecks:** Observing hotspots and load limits.
2. **Sharding Strategies:**
   - **User-Based Sharding:** Analyzing the "heavy user" problem.
   - **Channel-Based Sharding:** Analyzing the "viral channel" problem.
   - **Hash-Based Sharding:** Distributing load securely using composite keys.
3. **Stress & Spikes:** Simulating extreme traffic spikes to test hash distribution.
4. **Resiliency Testing:** Witnessing how outages drop data (missing shards/lost messages).
5. **Cross-Shard Querying:** Fetching recent cross-shard data requires querying every node, merging, and sorting (reduces efficiency to guarantee correctness).

## Final Analysis

The complete breakdown of strategy limits, data loss scenarios, and query problems is documented plainly in:
- `FINAL_ANALYSIS.txt`

## How to Run

1. Ensure you have Python 3 installed.
2. Run the simulation script from your terminal:
   ```bash
   python main.py
   ```
   *(Or try `python3 main.py` if `python` points to an older version.)*
3. Observe the output detailing the testing phases, the failure simulations, and lastly, the **Cross-Shard Query Test**.
