from discord import VoiceClient
from discord.gateway import DiscordVoiceWebSocket
import nacl.secret

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
        print("aaa")
        if not self.ws.record_ready:
            print("Not Record Ready")
            raise ValueError("Not Record Ready")
        
        while True:
            recv = await self.loop.sock_recv(self.socket,2**16)
            print(recv)

    async def connect_websocket(self) -> MyVoiceWebSocket:
        ws = await MyVoiceWebSocket.from_client(self)
        self._connected.clear()
        while ws.secret_key is None:
            await ws.poll_event()
        self._connected.set()
        return ws
    
    #---------- xsalsa20_poly1305 decrypt ----------------
    def decrypt_xsalsa20_poly1305(self,data: bytes)->tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted = data[:8],data[8:]
            nonce = bytearray(24)
            nonce[:8] = header
        else:
            header, encrypted = data[:12], data[12:]
            nonce = bytearray(24)
            nonce[:12] = header
        return header, box.decrypt(bytes(encrypted), bytes(nonce))
