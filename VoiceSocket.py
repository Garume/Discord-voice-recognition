import asyncio
from discord import VoiceClient
from discord.gateway import DiscordVoiceWebSocket
import nacl.secret
from PacketQueue import BufferDecoder

from RTCPacket import RTCPacket

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
        self.decoder = None
        self.is_recording = False

    #---------- record ----------------
    async def record(self,record_time=5):
        if self.is_recording:
            raise ValueError("Already recording")
        
        self.decoder= None
        self.is_recording = True
        self.decoder = BufferDecoder()
        
        self.record_task = self.loop.create_task(self.recv_voice_packet())
        await asyncio.sleep(record_time)

        self.record_task.cancel()

        self.record_task = None
        self.is_recording = False
        
        audio = await self.decoder.decode()
        print(audio.getvalue())
        with open("test.bin",mode = "wb") as f:
            f.write(audio.getvalue())
            
        return audio

    #---------- packet ----------------
    async def recv_voice_packet(self):
        print("aaa")
        if not self.ws.record_ready:
            print("Not Record Ready")
            raise ValueError("Not Record Ready")
        
        while True:
            recv = await self.loop.sock_recv(self.socket,2**16)

            if 200 <= recv[1] < 205:
                continue
            decrypt_func = getattr(self,f'decrypt_{self.mode}')
            header,data = decrypt_func(recv)
            packet = RTCPacket(header,data)
            packet.set_real_time()
            packet.calc_extension_header_length()
            
            self.decoder.recv_packet(packet)

    #---------- connect to vc socket ----------------
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

    def decrypt_xsalsa20_poly1305_suffix(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, nonce = data[:8], data[8:-24], data[-24:]
        else:
            header, encrypted, nonce = data[:12], data[12:-24], data[-24:]
        return header, box.decrypt(bytes(encrypted), bytes(nonce))

    def decrypt_xsalsa20_poly1305_lite(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, _nonce = data[:8], data[8:-4], data[-4:]
        else:
            header, encrypted, _nonce = data[:12], data[12:-4], data[-4:]
        nonce = bytearray(24)
        nonce[:4] = _nonce
        return header, box.decrypt(bytes(encrypted), bytes(nonce))
