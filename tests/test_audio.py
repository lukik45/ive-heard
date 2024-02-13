import pyaudio
from __config import HOST_DEVICE_TYPE



def __test_mac(p):
    def is_blackhole_present():
        for device_id in range(p.get_device_count()):
            device = p.get_device_info_by_index(device_id)
            if "BlackHole 2ch" in device["name"]:
                return True
        raise Exception("BlackHole 2ch not found")
    def is_multi_output_device_default():
        if p.get_default_output_device_info()["name"] == "Multi-Output Device":
            return True
        raise Exception("Multi-Output is not set as default")
    
    is_blackhole_present()
    is_multi_output_device_default()   


def test_audio(p):

    if HOST_DEVICE_TYPE == "mac":
        __test_mac(p)
    elif HOST_DEVICE_TYPE == "windows":
        raise NotImplementedError
    else:
        raise ValueError
