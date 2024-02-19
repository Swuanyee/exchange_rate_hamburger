# HamburgerExchangeRate 
This project automates the download and update of exchange rates from an Excel file into a local database, ensuring financial data is current. It handles file downloads, data parsing, and database operations.

## Features
- **Automatic Download**: Downloads `exchange_rates.xlsx` from a specified URL.
- **Retry Mechanism**: Retries download up to 5 times if the file isn't initially found.
- **Database Update**: Parses the Excel file and updates exchange rates in a SQLite database.
- **Clean-Up**: Deletes the Excel file post-update to maintain a clean workspace.

## Prerequisites
Ensure you have Python 3.x installed, along with the following packages:
- `requests` for HTTP requests.
- `openpyxl` for reading Excel files.
- `SQLAlchemy` for database operations.

## Installation
1. Clone this repository.
    ```bash
    git clone Swuanyee/HamburgerExchangeRate 
    ```
2. Install required Python packages.
    ```bash
    pip install -r requirements.txt 
    ```

## Usage
Run the script with:
```bash
python main.py
```
The script will automatically handle the download, data update, and file deletion processes.

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or enhancements.

## License
Distributed under the MIT License. See `LICENSE` for more information.

---

This README provides a basic overview to get started with the Exchange Rate Updater project, its features, installation steps, usage instructions, and contribution guidelines. Adjust the `<repository-url>` and other specific details as necessary for your project.