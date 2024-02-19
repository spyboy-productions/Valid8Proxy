import requests
import time
import sys
import os
from colorama import Fore, Style, init
from threading import Thread, Lock

init(autoreset=True)
print_lock = Lock()
stop_code = False

twitter_url = 'https://spyboy.in/twitter'
discord = 'https://spyboy.in/Discord'
website = 'https://spyboy.in/'
blog = 'https://spyboy.blog/'
github = 'https://github.com/spyboy-productions/Valid8Proxy'

VERSION = '0.0.1'

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
Y = '\033[33m'  # yellow

banner = r'''                                                    
  ___ ___       __ __    __ _______ _______                        
 |   Y   .---.-|  |__.--|  |   _   |   _   .----.-----.--.--.--.--.
 |.  |   |  _  |  |  |  _  |.  |   |.  1   |   _|  _  |_   _|  |  |
 |.  |   |___._|__|__|_____|.  _   |.  ____|__| |_____|__.__|___  |
 |:  1   |                 |:  1   |:  |                    |_____|
  \:.. ./                  |::.. . |::.|                           
   `---'                   `-------`---'                                                                               
      fetching, validating, and storing working proxies.     

'''

def print_banners():
    """
    prints the program banners
    """
    print(f'{G}{banner}{W}\n')
    print(f'{G}[+] {Y}Version      : {W}{VERSION}')
    print(f'{G}[+] {Y}Created By   : {W}Spyboy')
    print(f'{G} ╰➤ {Y}Twitter      : {W}{twitter_url}')
    print(f'{G} ╰➤ {Y}Discord      : {W}{discord}')
    print(f'{G} ╰➤ {Y}Website      : {W}{website}')
    print(f'{G} ╰➤ {Y}Blog         : {W}{blog}')
    print(f'{G} ╰➤ {Y}Github       : {W}{github}\n')

def fetch_proxies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        proxy_ips = []
        for line in response.text.split('\n'):
            parts = line.strip().split(':')
            if len(parts) == 2:
                ip, port = parts
                if ip.count('.') == 3 and port.isdigit():
                    proxy_ips.append(f'{ip}:{port}')

        return proxy_ips

    except requests.exceptions.RequestException as e:
        with print_lock:
            print(f'Error fetching proxies from {url}: {Fore.RED}{str(e)}{Style.RESET_ALL}')
        return []

def is_proxy_working(proxy):
    try:
        response = requests.get("https://www.example.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        response.raise_for_status()
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        with print_lock:
            print(f'Error validating proxy {proxy}: {Fore.RED}{str(e)}{Style.RESET_ALL}')
        return False

def validate_and_print_proxies(proxy_ips, print_limit=None):
    global stop_code
    working_proxies = set()  # Use a set to store unique working proxies
    printed_count = 0

    for proxy in proxy_ips:
        if printed_count >= print_limit:
            break

        thread = Thread(target=validate_and_print_proxy, args=(proxy, working_proxies, print_limit))
        thread.start()
        thread.join()

    return working_proxies

def validate_and_print_proxy(proxy, working_proxies, print_limit):
    global stop_code
    if not stop_code and is_proxy_working(proxy):
        with print_lock:
            print(f"Working Proxy IP: {Fore.GREEN}{proxy}{Style.RESET_ALL}")
            working_proxies.add(proxy)
            printed_count = len(working_proxies)
            if printed_count >= print_limit:
                stop_code = True

def save_proxies_to_file(proxies, filename="proxies.txt"):
    with open(filename, "w") as file:
        file.writelines([f"{proxy}\n" for proxy in proxies])

def main():
    print_banners()
    print(f"{C}Let's find some validated proxies!{W}")
    try:
        num_proxies_to_print = int(input(f"{W}Enter the number of proxies you want to print: {Y}"))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        sys.exit(1)

    start_time = time.time()
    proxy_urls = [
        'https://www.sslproxies.org/',
        'https://www.google-proxy.net/',
        'https://free-proxy-list.net/anonymous-proxy.html',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://www.us-proxy.org/',
        'https://free-proxy-list.net/'
    ]

    proxy_ips = []

    for url in proxy_urls:
        proxy_ips.extend(fetch_proxies(url))

    working_proxies = validate_and_print_proxies(proxy_ips, print_limit=num_proxies_to_print)

    print("\nList of Working Proxies:")
    for proxy in working_proxies:
        print(f"{Fore.GREEN}{proxy}{Style.RESET_ALL}")

    save_proxies_to_file(working_proxies)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken: {elapsed_time} seconds")

    current_directory = os.getcwd()
    save_path = os.path.join(current_directory, "proxies.txt")
    print(f"\nList of Working Proxies saved at: {Fore.YELLOW}{save_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
