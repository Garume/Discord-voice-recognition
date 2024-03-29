from discord.opus import Decoder
from discord.opus import exported_functions,OpusError,c_float_ptr
import sys,ctypes,os,logging,struct

log = logging.getLogger(__name__)

_lib = None

def libopus_loader(name):
    lib = ctypes.cdll.LoadLibrary(name)

    for item in exported_functions:
        func = getattr(lib,item[0])

        try:
            if item[1]:
                func.argtypes = item[1]
            func.restype = item[2]
        except KeyError:
            pass

        try:
            if item[3]:
                func.errcheck = item[3]
        except KeyError:
            log.exception("Error assigning "+func)
        
    return lib

def _load_default():
    global _lib
    try:
        if sys.platform == 'win32':
            _bitness = struct.calcsize('P') * 8
            _target = 'x64' if _bitness > 32 else 'x86'
            _filename = os.path.join('bin', 'libopus-0.{}.dll'.format(_target))
            _lib = libopus_loader(_filename)
        else:
            _lib = libopus_loader(ctypes.util.find_library('opus'))
    except Exception as e:
        print("opus_libの読み込みに失敗しました",e)
        _lib = None   
    
    return _lib is not None

def is_loaded():
    global _lib
    return _lib is not None

class MyDecoder(Decoder):
    @staticmethod
    def packet_get_nb_channels(data:bytes) -> int:
        return 2
    
    def decode_float(self,data,*,fec=False):
        if not is_loaded():
            _load_default()
        if data is None and fec:
            raise OpusError("Invalid arg")
        if data is None:
            frame_size = self._get_last_packet_duration() or self.SAMPLES_PER_FRAME
            channel_count = self.CHANNELS
        else:
            frames = self.packet_get_nb_frames(data)
            channel_count = self.packet_get_nb_channels(data)
            samples_per_frame = self.packet_get_samples_per_frame(data)
            frame_size = frames * samples_per_frame
            
        pcm = (ctypes.c_float * (frame_size * channel_count))()
        pcm_ptr = ctypes.cast(pcm, c_float_ptr)

        ret = _lib.opus_decode_float(self._state, data, len(data) if data else 0, pcm_ptr, frame_size, fec)

        return pcm[:ret * channel_count]