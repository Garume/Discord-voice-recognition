from collections import defaultdict

class PacketQueue:
    def __init__(self):
        self.queues = defaultdict(list)
    
    def push(self,packet):
        self.queues[packet.ssrc].append(packet)

class BufferDecoder:
    def __init__(self):
        self.queue = PacketQueue()
    
    def recv_packet(self,packet):
        self.queue.push(packet)