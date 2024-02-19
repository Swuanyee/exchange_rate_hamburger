from download_excel import download_excel
from store_rates import store_exchange_rates
import time
import os


def main():
    file_url = 'https://onedrive.live.com/download.aspx?resid=434F042447E4C39F!136&authkey=!AAsggaZW07MMJvE'
    local_filename = 'exchange_rates.xlsx'
    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        # Attempt to download the file
        download_excel(file_url, local_filename)

        # Wait for 15 seconds
        print(f"Waiting for 15 seconds before checking the file. Attempt {attempt + 1}/{max_attempts}")
        time.sleep(15)

        # Check if the file exists
        if os.path.exists(local_filename):
            print(f"File found: {local_filename}")

            # File found, proceed to read and update the database
            store_exchange_rates()

            # After successfully updating the exchange rates, delete the file
            try:
                os.remove(local_filename)
                print(f"File {local_filename} deleted successfully after updating the exchange rates.")
            except OSError as e:
                print(f"Error: {e.strerror}. File {local_filename} could not be deleted.")

            break
        else:
            print(f"File not found: {local_filename}. Retrying...")
            attempt += 1

    if attempt == max_attempts:
        print("Maximum download attempts reached. Exiting.")


if __name__ == "__main__":
    main()