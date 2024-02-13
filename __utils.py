

def get_input_device_index(p) -> int:
    """Returns the index of the input device. depending on the device, this may be a constant or a function.

    Returns:
        int: index of the input device
    """
    for device_id in range(p.get_device_count()):
        device = p.get_device_info_by_index(device_id)
        if "BlackHole 2ch" in device["name"]:
            return device_id
            
    raise Exception("BlackHole 2ch not found")