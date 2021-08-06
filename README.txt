Welcome to the 65EP5G Keypress Demo app. This application allows for calling of Remote Control API requests triggered by a keypress. The application can be run using the "start" scripts, and the source is available for modification or duplication.

Installation:

This application requires Python>=3.7. Please find the latest release at https://www.python.org/downloads/ and follow the instructions for your Operating System. When installing on Windows, check the option to "Add Python to PATH" and "Disable PATH length limit." Verify the most recent version on your system is invoked from the command line. You can check this by using 'py -V' on Windows or 'python3 -V' on MacOS.

Windows:
Double click start.bat. This will install all dependencies and start the script.

MacOS:
1. Open Terminal.
2. Type "sh " into the prompt (including the space) and then drag "start.sh" into the prompt. Press return.
3. MacOS will request permissions to allow the script to access the keyboard. Follow the prompts to grant permissions. This will require Terminal to close.
4. Open Terminal again.
5. Type "sh " into the prompt (including the space) and then drag "start.sh" into the prompt. Press return. This is how you will activate the script in the future.


Configuration:
The application can be configured by editing the config.txt file.

IP configuration:
Assign the IP of the 65EP5G to the ip field in config.txt.
Example:
ip = '192.168.1.10'

Key configuration:
Commands can be assigned by modifying the command_dictionary in config.txt. The provided config.txt has all possible API requests assigned to keys. Keys are defined according to Pynput Keys which are enumerated here: https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
By default:
Profiles 1-10 are assigned to keys 1-0.
Directional keys (up, down, left, right) and enter are assigned to the arrow keys and enter/return.
Back is assigned to backspace/delete, exit is assigned to x, and menu is assigned to m.
Function keys are assigned to F1-F5.
Print inputs is assigned to p.
Input selections are assigned to qwer... ...asdf (excluding p).