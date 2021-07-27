# Requires Python>=3.7

# API libraries
import websockets
import asyncio
import json

# Key input library (CASE SENSITIVE)
from pynput.keyboard import Listener, Key

# Standard libraries
import threading
import logging
import sys
import os

# Locals
import exceptions
import manifests
import commands
import helpers

# PIN input global
global keyboardinput
keyboardinput = ""

# Key set global
global current_keys
current_keys = set()

# Connection config
ip = '192.168.1.10'  # This default IP will be overwritten by ../config.txt
use_registered_key = True  # This default preference will also be overwritten


async def command_template():
    """
    Command template

    Because this websocket connection must executed in a synchronous flow, we have to reregester for each async.
    This template provides flexility in logic and execution that is not available in the send_command function so that you can create macros better suited to your specific needs.
    """
    try:
        async with websockets.connect('ws://' + ip + ':3000/', timeout=100) as ws:
            ck = helpers.read_client_key()
            cmd = commands.generate_registration(
                manifests.custom_manifest, ck)
            await ws.send(json.dumps(cmd))
            greeting = await ws.recv()
            decoded = json.loads(greeting)
            if decoded['type'] == 'registered':
                client_key = decoded['payload']['client-key']
                helpers.update_client_key(client_key)
            else:
                helpers.resp_print(greeting)
                print('Command registration failed. Please reconnect.')
                helpers.remove_client_key()
                await reg_script()

            # YOUR COMMAND/FUNCTION GOES HERE
    except:
        print('Command registration failed, please relaunch the script.')
        helpers.remove_client_key()


async def send_command(command_to_send, verbose=False):
    """
    Websocket send for default command set

    Args:
        command_to_send: A JSON object to be sent to the display
        verbose: Whether to print the display's response, even if there isn't an error
    """
    try:
        async with websockets.connect('ws://' + ip + ':3000/', timeout=100) as ws:
            ck = helpers.read_client_key()
            cmd = commands.generate_registration(
                manifests.custom_manifest, ck)
            await ws.send(json.dumps(cmd))
            greeting = await ws.recv()
            decoded = json.loads(greeting)
            if decoded['type'] == 'registered':
                client_key = decoded['payload']['client-key']
                helpers.update_client_key(client_key)
            else:
                helpers.resp_print(greeting)
                print('Command registration failed. Please reconnect.')
                helpers.remove_client_key()
                await reg_script()

            await ws.send(json.dumps(command_to_send))

            resp = await ws.recv()
            helpers.resp_print(resp)
            if verbose:
                print(resp)
    except:
        print('Command registration failed, please relaunch the script.')
        helpers.remove_client_key()


# Command sending helpers
def keypress(button):
    asyncio.run(send_command(commands.key_command(button)))


def send_input(select):
    asyncio.run(send_command(commands.set_input(select)))


def select_profile(index):
    asyncio.run(send_command(commands.load_profile(index), False))


def print_inputs():
    asyncio.run(send_command(commands.get_input_list, verbose=True))


# Dictionary-callable commands
def left():
    keypress('LEFT')


def right():
    keypress('RIGHT')


def up():
    keypress('UP')


def down():
    keypress('DOWN')


def enter():
    keypress('ENTER')


def menu():
    keypress('MENU')


def back():
    keypress('BACK')


def exit():
    keypress('EXIT')


def f1():
    keypress('functionKey1')


def f2():
    keypress('functionKey2')


def f3():
    keypress('functionKey3')


def f4():
    keypress('functionKey4')


def f5():
    keypress('functionKey5')


def safety_area():
    keypress('safetyArea')


def profile_1():
    select_profile(1)


def profile_2():
    select_profile(2)


def profile_3():
    select_profile(3)


def profile_4():
    select_profile(4)


def profile_5():
    select_profile(5)


def profile_6():
    select_profile(6)


def profile_7():
    select_profile(7)


def profile_8():
    select_profile(8)


def profile_9():
    select_profile(9)


def profile_10():
    select_profile(10)


def set_hdmi1():
    send_input('HDMI_1')


def set_hdmi2():
    send_input('HDMI_2')


def set_sdi1():
    send_input('SDI_1')


def set_sdi2():
    send_input('SDI_2')


def set_sdi3():
    send_input('SDI_3')


def set_sdi4():
    send_input('SDI_4')


def set_sdi_dual12():
    send_input('SDI_DUAL_12')


def set_sdi_dual34():
    send_input('SDI_DUAL_34')


def set_sdi_quad_auto():
    send_input('SDI_QUAD_AUTO')


def set_sdi_quad_2SI():
    send_input('SDI_QUAD_2SI')


def set_sdi_quad_square():
    send_input('SDI_QUAD_SQUARE')


def set_sdi_quad_view():
    send_input('SDI_QUAD_VIEW')


def set_sfp():
    send_input('SFP+')


# This default dictionary will be overwritten by a dictionary by the same name in config.py
command_dictionary = {
    '1':            profile_1,
    '2':            profile_2,
    '3':            profile_3,
    '4':            profile_4,
    '5':            profile_5,
    '6':            profile_6,
    '7':            profile_7,
    '8':            profile_8,
    '9':            profile_9,
    '0':            profile_10,
    Key.left:       left,
    Key.right:      right,
    Key.up:         up,
    Key.down:       down,
    Key.enter:      enter,
    Key.backspace:  back,
    'x':            exit,
    'm':            menu,
    Key.f1:         f1,
    Key.f2:         f2,
    Key.f3:         f3,
    Key.f4:         f4,
    Key.f5:         f5,
    'p':            print_inputs,
    'q':            set_hdmi1,
    'w':            set_hdmi2,
    'e':            set_sdi1,
    'r':            set_sdi2,
    't':            set_sdi3,
    'y':            set_sdi4,
    'u':            set_sdi_dual12,
    'i':            set_sdi_dual34,
    'o':            set_sdi_quad_auto,
    'a':            set_sdi_quad_2SI,
    's':            set_sdi_quad_square,
    'd':            set_sdi_quad_view,
    'f':            set_sfp
}


class WaitforKeyInput(threading.Thread):
    '''Class for async key input support.'''

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        global keyboardinput
        try:
            if self.kwargs.get('keytype') == 'any':
                keyin = input()
            elif self.kwargs.get('keytype') == 'number':
                keyin = ""
                while not keyin.isnumeric():
                    keyin = input()
            elif self.kwargs.get('keytype') == 'number_q':
                keyin = ""
                while True:
                    keyin = input()
                    if not keyin.isnumeric() and keyin != 'q':
                        print(helpers.TextColorCode.WARNING
                              + "Invalid input. It must be number or q:"
                              + helpers.TextColorCode.ENDC, end='')
                    else:
                        break
            elif self.kwargs.get('keytype') == 'pin':
                keyin = ""
                while True:
                    keyin = input()
                    if keyin.isnumeric() and len(keyin) == 8:
                        break
                    else:
                        print("Invalid input. It must be 8 digits: ", end='')
            elif self.kwargs.get('keytype') == 'list':
                valid_input = self.kwargs.get('validInput')
                keyin = ''
                while True:
                    keyin = input()
                    if keyin not in valid_input:
                        print(helpers.TextColorCode.WARNING
                              + "Invalid input. It must be one of {0}: ".format(valid_input)
                              + helpers.TextColorCode.ENDC, end='')
                    else:
                        break
            else:  # if user just hit ENTER, it is ignored
                keyin = ""
                print("should not be here")
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        finally:
            pass
        # now we received some key input
        keyboardinput = keyin


async def reg_script():
    """Performs the initial registration with the TV, storing the client key to be used for future commands."""
    greeting = ''
    try:
        async with websockets.connect('ws://' + ip + ':3000/', timeout=100) as websocket:
            pin_accepted = False
            while not pin_accepted:
                # send appropriate register cmd
                if use_registered_key:
                    ck = helpers.read_client_key()
                    cmd = commands.generate_registration(
                        manifests.custom_manifest, ck)
                else:
                    cmd = commands.generate_registration(
                        manifests.custom_manifest)

                if not greeting:
                    await websocket.send(json.dumps(cmd))

                # receive prompt
                greeting = await websocket.recv()
                helpers.resp_print(greeting)
                decoded = json.loads(greeting)

                # stored key is accepted
                if decoded['type'] == 'registered':
                    client_key = decoded['payload']['client-key']
                    helpers.update_client_key(client_key)
                    print('Registered, key stored')
                    pin_accepted = True

                # stored key is rejected
                if (not pin_accepted) and use_registered_key:
                    helpers.remove_client_key()

                # display chooses to do a prompt for some reason
                if decoded['type'] == 'response' and decoded['payload']['pairingType'] == 'PROMPT':
                    print('Please accept the prompt on the 65EP5G.')
                    greeting = await websocket.recv()
                    helpers.resp_print(greeting)
                    decoded = json.loads(greeting)
                    if decoded['type'] == 'registered':
                        client_key = decoded['payload']['client-key']
                        helpers.update_client_key(client_key)
                        print('Registered, key stored')
                        pin_accepted = True
                    else:
                        print('Prompt rejected.')

                # try pin pairing
                if not pin_accepted:
                    if decoded['type'] == 'error':
                        # There was an error on the previous attempt, start reg from the top
                        raise exceptions.ConnectionFailed
                    elif not (decoded['payload']['pairingType'] == 'PIN' and decoded['payload']['returnValue']):
                        # There wasn't an error, but we don't have the pin prompt, request again
                        cmd = commands.generate_registration(
                            manifests.custom_manifest)
                        await websocket.send(json.dumps(cmd))
                    else:
                        # We have a prompt and
                        print('Enter PIN (8-digit) shown on TV screen here:', end='')
                        thread_t = WaitforKeyInput(
                            args=(0,), kwargs={'keytype': 'pin'})
                        thread_t.start()
                        while thread_t.is_alive():
                            await asyncio.sleep(0.5)

                        pin_cmd = commands.send_pin_template
                        pin_cmd['payload']['pin'] = keyboardinput
                        await websocket.send(json.dumps(pin_cmd))

                        # receive prompt
                        greeting = await websocket.recv()
                        helpers.resp_print(greeting)
                        decoded = json.loads(greeting)
                        if decoded['type'] == 'registered':
                            client_key = decoded['payload']['client-key']
                            helpers.update_client_key(client_key)
                            print('Registered, key stored')
                            pin_accepted = True
    except exceptions.ConnectionFailed:
        print('Connection failed - retrying. Likely PIN was incorrectly entered.')
        await reg_script()
    except TimeoutError:
        print('Timeout error - check IP address of the TV')
    except ConnectionRefusedError:
        print('ConnectionRefused error - check IP address of the TV')
    except websockets.exceptions.ConnectionClosed:
        print('websockets.exceptions.ConnectionClosed - timeout or wrong PIN entered')
    except KeyboardInterrupt:
        print('Ctrl-C hit')
    finally:
        pass


def keyboard_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def key_cleaner(key):
    try:
        return key.char
    except AttributeError:
        return key


def on_press(key):
    key = key_cleaner(key)
    current_keys.add(key)


def on_release(key):
    key = key_cleaner(key)

    to_execute = command_dictionary.get(key)
    if to_execute:
        to_execute()
        print('ran ' + to_execute.__name__)

    if key in current_keys:
        current_keys.remove(key)


async def main():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, keyboard_listener)


# required for async compatibility
assert sys.version_info >= (3, 7)

# read and run config
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, '..', 'config.txt'))
exec(open(filepath, 'r').read())

# if we aren't using the registered key, delete it now
if not use_registered_key:
    helpers.remove_client_key()

# check device exists at given IP
if helpers.ping(ip):
    try:
        asyncio.run(reg_script())
        asyncio.run(main())
    except:
        print('Error: Please ensure the 65EP5G is on the same local network as this machine and there are no firewalls/subnet masks preventing the connection.')
else:
    print('Display not found at provided address. Please verify address and network configuration and try again.')
