import random
from message import Message
from server import ChatServer
from shards import ShardManager, HashShardManager

NUM_USERS    = 50000
NUM_CHANNELS = 10
NUM_MESSAGES = 100000
NUM_SHARDS   = 5

def simulate_naive():
    server = ChatServer()
    for _ in range(NUM_MESSAGES):
        user_id    = random.randint(1, NUM_USERS)
        channel_id = 1 if random.random() < 0.8 else random.randint(2, NUM_CHANNELS)
        server.send_message(Message(user_id, channel_id, "hello"))
    server.stats()

def simulate_user_sharding():
    mgr = ShardManager(NUM_SHARDS)
    heavy_user = 1
    for _ in range(NUM_MESSAGES):
        user_id    = heavy_user if random.random() < 0.7 else random.randint(2, NUM_USERS)
        channel_id = random.randint(1, NUM_CHANNELS)
        mgr.route_by_user(Message(user_id, channel_id, "hello"))
    mgr.stats("user-based sharding | heavy user=1")

def simulate_channel_sharding():
    mgr = ShardManager(NUM_SHARDS)
    for _ in range(NUM_MESSAGES):
        user_id    = random.randint(1, NUM_USERS)
        channel_id = 1 if random.random() < 0.8 else random.randint(2, NUM_CHANNELS)
        mgr.route_by_channel(Message(user_id, channel_id, "hello"))
    mgr.stats("channel-based sharding | viral channel=1")

def simulate_hash_sharding():
    mgr = HashShardManager(NUM_SHARDS)
    heavy_user = 1
    for _ in range(NUM_MESSAGES):
        user_id    = heavy_user if random.random() < 0.2 else random.randint(2, NUM_USERS)
        channel_id = 1 if random.random() < 0.8 else random.randint(2, NUM_CHANNELS)
        mgr.route_by_hash(Message(user_id, channel_id, "hello"))
    mgr.stats("hash-based sharding | composite key")

def stress_test(manager, label, num_users, num_channels, num_messages, viral=False, heavy_user=False):
    heavy_u_id = 1
    viral_c_id = 1
    for _ in range(num_messages):
        user_id = heavy_u_id if heavy_user and random.random() < 0.8 else random.randint(2, max(2, num_users))
        channel_id = viral_c_id if viral and random.random() < 0.8 else random.randint(2, max(2, num_channels))
        
        msg = Message(user_id, channel_id, "hello")
        if isinstance(manager, HashShardManager):
            manager.route_by_hash(msg)
        elif "channel" in label.lower():
            manager.route_by_channel(msg)
        else:
            manager.route_by_user(msg)
            
    manager.stats(label)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("PHASE 1 — Naive Single Server (hotspot visible)")
    print("="*50)
    simulate_naive()

    print("\n" + "="*50)
    print("PHASE 2 — User-Based Sharding (heavy user problem)")
    print("="*50)
    simulate_user_sharding()

    print("\n" + "="*50)
    print("PHASE 3 — Channel-Based Sharding (viral channel problem)")
    print("="*50)
    simulate_channel_sharding()

    print("\n" + "="*50)
    print("PHASE 4 — Hash-Based Sharding")
    print("="*50)
    simulate_hash_sharding()

    print("\n" + "="*50)
    print("PHASE 5 — Stress Testing Scenarios")
    print("="*50)
    
    stress_test(HashShardManager(NUM_SHARDS), "Normal Load", NUM_USERS, NUM_CHANNELS, NUM_MESSAGES)
    stress_test(HashShardManager(NUM_SHARDS), "Viral Event", NUM_USERS, NUM_CHANNELS, NUM_MESSAGES, viral=True)
    stress_test(HashShardManager(NUM_SHARDS), "Extreme Spike", NUM_USERS, NUM_CHANNELS, NUM_MESSAGES * 2, viral=True, heavy_user=True)

    print("\n" + "="*50)
    print("FAILURE TEST — Shard 2 Down")
    print("="*50)
    
    mgr_fail = HashShardManager(NUM_SHARDS)
    mgr_fail.disable_shard(2)
    # Using 10000 messages to avoid completely flooding the output with lost message prints
    stress_test(mgr_fail, "Failure Test - Viral Traffic", NUM_USERS, NUM_CHANNELS, 10000, viral=True)
