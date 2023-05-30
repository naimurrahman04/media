import os
import platform
import subprocess
import sys
import urllib.request
import socket
output = ''
# Get the path of the Python interpreter
current_dir = os.getcwd()
pid = os.getpid()
process_name = os.path.basename(__file__)
executable_path = sys.executable

output += f'Current working directory: {current_dir}\n'   
output += f'Process ID: {pid}\n'
output += f'Process name: {process_name}\n'
output += f'Executable path: {executable_path}\n'

print(f'Current working directory: {current_dir}\n')
print( f'Process ID: {pid}\n')
print(f'Process name: {process_name}\n')
print(f'Executable path: {executable_path}\n')
script_path = os.path.abspath(__file__)
print("The script is located at:", script_path)