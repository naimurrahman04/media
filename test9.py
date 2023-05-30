import os
import subprocess


# Get the path of the current script
script_path = os.path.abspath(__file__)

# Start the script in the background
result = subprocess.run([script_path], stdout=subprocess.PIPE, shell=True)

with open("myfile.txt", "w") as f:
    f.write("hello")


