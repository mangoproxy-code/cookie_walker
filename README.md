# Cookie Walker

This project is a Python-based GUI application that visits a list of URLs using a specified proxy configuration, collects cookies from the visited sites, and saves them in a JSON file. It also displays the results on an interactive map.

## Features

- GUI for easy input of proxy configuration and URL list
- Supports SOCKS5 proxies and direct connections
- Concurrent URL visits for faster cookie collection
- Progress bar to show the progress
- Real-time log updates
- Stop and save functionality
- Interactive map with visited URLs
- JSON output of collected cookies

## Prerequisites

- Python 3.x
- aiohttp
- aiofiles
- folium
- tkinter
- aiohttp_socks

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mangoproxy-code/cookie_walker.git
    cd cookie_walker
    ```

2. Install the required Python packages:
    ```sh
    pip install aiohttp aiofiles folium aiohttp_socks
    ```

## Usage

1. Run the `profile_warming.py` script:
    ```sh
    python profile_warming.py
    ```

2. Use the GUI to:
    - Input your proxy configuration in the format `user:password@host:port`.
    - Browse and select the file containing the URLs.
    - Click "Start" to begin the process.
    - Click "Stop and Save" to stop the process and save the results.
    - Click "Open Map" to view the interactive map.
    - Click "Open JSON" to view the JSON file with the results.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Alex Whynot
