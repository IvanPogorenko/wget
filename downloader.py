import os
import sys
import http.client
import time
from urllib.parse import urlparse

def download_file(url):
    parsed_url = urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc) if parsed_url.scheme == 'https' else http.client.HTTPConnection(parsed_url.netloc)

    conn.request('GET', parsed_url.path)
    response = conn.getresponse()

    if response.status != 200:
        print(f"Не удалось загрузить файл: {response.status} {response.reason}")
        conn.close()
        return

    filename = os.path.basename(parsed_url.path) or 'downloaded_file'

    with open(filename, 'wb') as f:
        downloaded_bytes = 0

        start_time = time.time()
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            f.write(chunk)

            downloaded_bytes += len(chunk)

            if time.time() - start_time >= 1:
                print(f"Downloaded: {downloaded_bytes} bytes", end='\r')
                start_time = time.time()

    conn.close()
    print(f"\nФайл загружен как {filename}")

def main():
    if len(sys.argv) != 2:
        print("Использование: python download.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    download_file(url)

if __name__ == "__main__":
    main()
