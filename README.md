# Profile Warming Tool

This project is a Python-based GUI application to increase views on a profile by visiting a list of URLs, with the option to use a proxy or direct connection. It captures cookies from each visited URL.

## Features

- GUI for easy input of details
- Supports SOCKS5 proxies and direct connections
- Progress bar to show the progress
- Real-time log updates
- Real-time cookie capture and storage

## Prerequisites

- Python 3.x
- aiohttp
- aiofiles
- tkinter
- aiohttp_socks

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the `profile_warming.py` script:
    ```sh
    python profile_warming.py
    ```

2. Use the GUI to:
    - Input your proxy (if using a proxy) in the format `user:password@host:port`.
    - Toggle the "Use Proxy" checkbox based on your preference.
    - Browse and select the file containing the URLs.
    - Click "Start" to begin the profile warming process.

3. Check the `cookies.json` file for the collected cookies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
