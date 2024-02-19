import requests

def download_excel(file_url, local_filename):
    response = requests.get(file_url, stream=True)
    print("HTTP Status Code:", response.status_code)  # Print HTTP status code
    if response.ok:
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print(f"File downloaded and saved as {local_filename}")
    else:
        print(f"Failed to download file. HTTP Status: {response.status_code}")
        print("Response:", response.text[:500])  # Print first 500 characters of response text