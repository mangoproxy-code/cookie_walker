import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector
from random import randint
from tkinter import Tk, Label, Entry, Button, StringVar, Text, END, ttk, filedialog, Checkbutton, BooleanVar
from threading import Thread
import json
from datetime import datetime, timedelta
import webbrowser

# Define constants
NUM_CONCURRENT_TASKS = 100  # Increased concurrency
TIMEOUT = 5  # Timeout for requests in seconds

# GUI Class
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Profile Warming Tool")
        self.root.resizable(False, False)

        self.use_proxy = BooleanVar()
        self.use_proxy.set(True)  # Default to using a proxy

        self.proxy_label = Label(root, text="Proxy (user:password@host:port)")
        self.proxy_label.grid(row=0, column=0)
        self.proxy_entry = Entry(root, textvariable=StringVar())
        self.proxy_entry.grid(row=0, column=1)

        self.urls_label = Label(root, text="URLs File")
        self.urls_label.grid(row=1, column=0)
        self.urls_entry = Entry(root, textvariable=StringVar())
        self.urls_entry.grid(row=1, column=1)
        self.urls_button = Button(root, text="Browse", command=self.browse_urls)
        self.urls_button.grid(row=1, column=2)

        self.proxy_checkbutton = Checkbutton(root, text="Use Proxy", variable=self.use_proxy)
        self.proxy_checkbutton.grid(row=2, column=1)

        self.start_button = Button(root, text="Start", command=self.start)
        self.start_button.grid(row=3, column=1)

        self.mango_button = Button(root, text="Get Proxy from MangoProxy", command=self.open_mango_proxy)
        self.mango_button.grid(row=4, column=1)

        self.progress_label = Label(root, text="Progress")
        self.progress_label.grid(row=5, column=0)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=5, column=1)

        self.log_label = Label(root, text="Log")
        self.log_label.grid(row=6, column=0)
        self.log_text = Text(root, height=10, width=50)
        self.log_text.grid(row=7, column=0, columnspan=3)

    def browse_urls(self):
        self.urls_entry.delete(0, END)
        self.urls_entry.insert(0, filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]))

    def update_progress(self, value):
        self.root.after(0, self.progress.config, {'value': value})

    def update_log(self, message):
        self.root.after(0, self.log_text.insert, END, message + "\n")
        self.root.after(0, self.log_text.see, END)

    def start(self):
        use_proxy = self.use_proxy.get()
        proxy = self.proxy_entry.get() if use_proxy else None
        if proxy and not proxy.startswith("socks5://"):
            proxy = "socks5://" + proxy
        urls_file = self.urls_entry.get()

        self.progress['value'] = 0

        api = ProfileWarmer(proxy, urls_file, self.update_log, self.update_progress, use_proxy)
        Thread(target=lambda: asyncio.run(api.run())).start()

    def open_mango_proxy(self):
        webbrowser.open("https://dashboard.mangoproxy.com/signup?ref=soft")

# ProfileWarmer Class
class ProfileWarmer:
    def __init__(self, proxy, urls_file, update_log, update_progress, use_proxy):
        self.proxy = proxy
        self.urls_file = urls_file
        self.update_log = update_log
        self.update_progress = update_progress
        self.use_proxy = use_proxy
        self.success = 0
        self.failed = 0

    async def fetch(self, session, url, cookies):
        try:
            async with session.get(url, timeout=TIMEOUT) as response:
                await response.text()
                self.success += 1
                self.update_log(f"Successfully accessed {url}")
                cookie_jar = session.cookie_jar.filter_cookies(url)
                cookies[url] = [
                    {
                        'name': cookie.key,
                        'value': cookie.value,
                        'domain': cookie['domain'] if 'domain' in cookie else url,
                        'path': cookie['path'] if 'path' in cookie else '/',
                        'expiry': (datetime.now() + timedelta(days=30)).timestamp(),
                    }
                    for cookie in cookie_jar.values()
                ]
                await self.save_cookies(cookies)
        except Exception as e:
            self.failed += 1
            self.update_log(f"Failed to access {url}: {e}")

    async def warm_profile(self, urls, cookies):
        connector = ProxyConnector.from_url(self.proxy) if self.use_proxy else None
        async with ClientSession(connector=connector, cookie_jar=aiohttp.CookieJar()) as session:
            tasks = [self.fetch(session, url, cookies) for url in urls]
            await asyncio.gather(*tasks)

    async def load_urls(self):
        async with aiofiles.open(self.urls_file, mode='r') as f:
            urls = await f.readlines()
        return [url.strip() for url in urls]

    async def save_cookies(self, cookies):
        async with aiofiles.open('cookies.json', mode='w') as f:
            await f.write(json.dumps(cookies, indent=4))

    async def run(self):
        urls = await self.load_urls()
        total_urls = len(urls)
        cookies = {}
        self.update_progress(0)

        for i in range(0, total_urls, NUM_CONCURRENT_TASKS):
            batch = urls[i:i + NUM_CONCURRENT_TASKS]
            await self.warm_profile(batch, cookies)
            progress_value = (i + len(batch)) / total_urls * 100
            self.update_progress(progress_value)

        self.update_log(f"Completed with {self.success} successes and {self.failed} failures.")
        self.update_progress(100)

# Main function
if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
