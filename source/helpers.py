import subprocess
import platform
import json
import os


# Client key management
def update_client_key(new_client_key):
    f = open('source/client_key', 'wt')
    f.write(new_client_key)
    f.close()

def read_client_key():
    try:
        f = open('source/client_key', 'rt')
        l = f.readline()
        f.close()
        return l
    except OSError:
        print('No existing client key.')

def remove_client_key():
    if os.path.exists('source/client_key'):
            os.remove('source/client_key')


def resp_print(greeting):
    """
    Only print contents of error messages.

    Args:
        greeting: A JSON message from the display.
    """
    decoded = json.loads(greeting)
    if decoded['type'] == 'error':
        err_msg = decoded['error']
        err_msg = 'Error: ' + err_msg
        print(err_msg)


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    A host may not respond to a ping (ICMP) request even if the host name is valid, but this shouldn't be the case with the 65EP5G.
    May return false positives on Windows.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


# Formatting
class TextColorCode:  # pylint: disable=too-few-public-methods
    ''' text color code
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

