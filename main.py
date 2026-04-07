import random
from message import Message
from server import ChatServer
from shards import ShardManager

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
