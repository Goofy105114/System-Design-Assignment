from collections import defaultdict

class ChatServer:
    def __init__(self):
        self.messages = defaultdict(list)
        self.total = 0

    def send_message(self, message):
        self.messages[message.channel_id].append(message)
        self.total += 1

    def stats(self):
        print(f"\n=== ChatServer Stats ===")
        print(f"Total messages: {self.total}")
        for channel_id, msgs in sorted(self.messages.items()):
            pct = (len(msgs) / self.total) * 100
            bar = "█" * int(pct // 2)
            print(f"  channel {channel_id:>3}: {len(msgs):>6} msgs ({pct:5.1f}%) {bar}")
