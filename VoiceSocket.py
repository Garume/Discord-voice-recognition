from discord import VoiceClient
from discord.gateway import DiscordVoiceWebSocket

class MyVoiceWebSocket(DiscordVoiceWebSocket):
    def __init__(self, socket, loop):
        super().__init__(socket, loop)
        self.record_ready = False
    
    async def received_message(self, msg):
        await super(MyVoiceWebSocket,self).received_message(msg)
        op = msg['op']
        print(msg)

        if op == self.SESSION_DESCRIPTION:
            self.record_ready = True
        
class MyVoiceClient(VoiceClient):
    def __init__(self, client, channel):
        super().__init__(client, channel)
        self.record_task = None
    
    async def recv_voice_packet(self):
        if not self.ws.record_ready:
            raise ValueError("Not Record Ready")
        
        while True:
            recv = await self.loop.sock_recv(self.socket,2**16)
             
    async def connect_websocket(self) -> MyVoiceWebSocket:
        ws = await MyVoiceWebSocket.from_client(self)
        self._connected.clear()
        while ws.secret_key is None:
            await ws.poll_event()
        self._connected.set()
        return ws