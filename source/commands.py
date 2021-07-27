# Sets of parameters
normal_keys = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', 'MENU', 'BACK', 'EXIT']
function_values = ['undefined', 'marker', 'safetyArea', 'markerPreset1', 'markerPreset2',
                   'aspectRatio', 'audioLVMeter', 'MonoBlueOnly', 'waveform', 'vectorColor', 'EOTF', 'IPMode']
inputs = ['HDMI_1', 'HDMI_2', 'HDMI_3', 'SDI_1', 'SDI_2', 'SDI_2', 'SDI_3', 'SDI_DUAL_12',
          'SDI_DUAL_34', 'SDI_QUAD_AUTO', 'SDI_QUAD_2SI', 'SDI_QUAD_SQUARE', 'SDI_QUAD_VIEW', 'SFP+']


# General registration template
reg_template = {
    'type': 'register',
    'id': 1,
    'payload': {
            'client-key': '',
            'manifest': ''
    }
}

# Registration request using a PIN
reg_pin = {
    'type': 'register',
    'id': 1,
    'payload': {
        'client-key': '',
        'pairingType': 'PIN',
        'manifest': ''
    }
}

# Sends PIN to display with active prompt
send_pin_template = {
    "type": "request",
    "id": 1,
    "uri": "palm://pairing/setPin",
    "payload": {
        "pin": ""
    }
}

# Sets input on the display. Special formatting required for SDI and SFP. See set_input
input_template = {
    "type": "request",
    "id": 1,
    "uri": "ssap://tv/switchInput",
    "payload": {
        "inputId": "HDMI_1"
    }
}

# Sends a keypress to the display
keypress_template = {
    "type": "request",
    "id": 1,
    "uri": "luna://inputgenerator/pushKeyEvent",
    "payload": {
        "key": "functionKey1"
    }
}

# Loads a profile (Profiles integers 1-10)
load_profile_template = {
    "type": "request",
    "id": 1,
    "uri": "luna://inputgenerator/loadProfile",
    "payload": {
            "profile": 1
    }
}

# Prints the list of currently connected devices. Only has information for HDMI connections.
get_input_list = {
    "type": "request",
    "id": 1,
    "uri": "palm://tv/getExternalInputList"
}


def generate_registration(manifest, client_key=''):
    """Creates registration command using the provided manifest. Includes client key if provided, otherwise requests PIN pairing."""
    cmd = reg_template
    cmd['payload']['manifest'] = manifest
    if client_key:
        cmd['payload']['client-key'] = client_key
    else:
        cmd['payload']['pairingType'] = 'PIN'
    return cmd


def send_pin(pin):
    """Sends an entered pin to the display."""
    cmd = send_pin_template
    cmd['payload']['pin'] = pin
    return cmd

def set_input(source):
    """Sets the input. Uses the 'inputType' field for SDI and SFP inputs."""
    cmd = input_template
    if source == 'HDMI_1' or source == 'HDMI_2':
        cmd['payload']['inputId'] = source
    else:
        cmd['payload']['inputId'] = 'HDMI_3'
        cmd['payload']['inputType'] = source
    return cmd

def key_command(key, set_function=""):
    """Handles keypresses of normal and function keys, as well as assigning function keys."""
    cmd = keypress_template
    cmd['payload']['key'] = key
    if key not in normal_keys:
        cmd['uri'] = "luna://inputgenerator/pushFunctionKey"
        if set_function:
            cmd['payload']['setfunction'] = set_function
            cmd['uri'] = "luna://inputgenerator/setFunctionKey"
    return cmd

def load_profile(index):
    """Loads the given profile."""
    cmd = load_profile_template
    cmd['payload']['profile'] = index
    return cmd

