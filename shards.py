from collections import defaultdict
import hashlib

class Shard:
    def __init__(self, shard_id):
        self.shard_id = shard_id
        self.messages = defaultdict(list)
        self.total = 0
        self.active = True

    def store(self, message):
        self.messages[message.channel_id].append(message)
        self.total += 1

class ShardManager:
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shards = [Shard(i) for i in range(num_shards)]

    def get_shard(self, key):
        return self.shards[key % self.num_shards]

    def disable_shard(self, shard_id):
        if 0 <= shard_id < self.num_shards:
            self.shards[shard_id].active = False

    def _route(self, shard, message):
        if not shard.active:
            print(f"Shard {shard.shard_id} is down, message lost")
            return
        shard.store(message)

    def route_by_user(self, message):
        shard = self.get_shard(message.sender_id)
        self._route(shard, message)

    def route_by_channel(self, message):
        shard = self.get_shard(message.channel_id)
        self._route(shard, message)

    def stats(self, label=""):
        total = sum(s.total for s in self.shards)
        print(f"\n=== ShardManager Stats [{label}] ===")
        print(f"Total messages: {total}")
        for shard in self.shards:
            pct = (shard.total / total * 100) if total else 0
            bar = "█" * int(pct // 2)
            print(f"  shard {shard.shard_id}: {shard.total:>6} msgs ({pct:5.1f}%) {bar}")

class HashShardManager(ShardManager):
    def get_shard_by_hash(self, key):
        # Use md5 to ensure consistent hashing
        hash_val = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        return self.shards[hash_val % self.num_shards]

    def route_by_hash(self, message):
        key = f"{message.sender_id}-{message.channel_id}"
        shard = self.get_shard_by_hash(key)
        self._route(shard, message)
