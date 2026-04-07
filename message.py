import time

class Message:
    def __init__(self, sender_id, channel_id, content):
        self.sender_id = sender_id
        self.channel_id = channel_id
        self.content = content
        self.timestamp = time.time()

    def __repr__(self):
        return f"[ch:{self.channel_id}] user:{self.sender_id} => {self.content}"
