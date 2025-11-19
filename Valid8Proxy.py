from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse
import os
import re
import sys
import time
from threading import Event, Lock

import requests
from colorama import Fore, Style, init


VERSION = "0.0.6"
twitter_url = "https://spyboy.in/twitter"
discord = "https://spyboy.in/Discord"
website = "https://spyboy.in/"
blog = "https://spyboy.blog/"
github = "https://github.com/spyboy-productions/Valid8Proxy"
BANNER = r"""
  ___ ___       __ __    __ _______ _______
 |   Y   .---.-|  |__.--|  |   _   |   _   .----.-----.--.--.--.--.
 |.  |   |  _  |  |  |  _  |.  |   |.  1   |   _|  _  |_   _|  |  |
 |.  |   |___._|__|__|_____|.  _   |.  ____|__| |_____|__.__|___  |
 |:  1   |                 |:  1   |:  |                    |_____|
  \:.. ./                  |::.. . |::.|
   `---'                   `-------`---'
    fetching, validating, and storing working proxies.
"""

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
IPPORT_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}\b")
print_lock = Lock()



def print_banner():
    init(autoreset=True)
    print(Fore.MAGENTA + BANNER + Style.RESET_ALL)
    print(f"{Fore.GREEN}[+] {Fore.YELLOW}Version      : {Style.RESET_ALL}{VERSION}")
    print(f"{Fore.GREEN}[+] {Fore.YELLOW}Created By   : {Style.RESET_ALL}Spyboy")
    print(f"{Fore.GREEN} ╰➤ {Fore.YELLOW}Twitter      : {Style.RESET_ALL}{twitter_url}")
    print(f"{Fore.GREEN} ╰➤ {Fore.YELLOW}Discord      : {Style.RESET_ALL}{discord}")
    print(f"{Fore.GREEN} ╰➤ {Fore.YELLOW}Website      : {Style.RESET_ALL}{website}")
    print(f"{Fore.GREEN} ╰➤ {Fore.YELLOW}Blog         : {Style.RESET_ALL}{blog}")
    print(f"{Fore.GREEN} ╰➤ {Fore.YELLOW}Github       : {Style.RESET_ALL}{github}\n")


def fetch_proxies_from_url(url, session, timeout=10):

    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        text = resp.text
        matches = set(IPPORT_RE.findall(text))
        return list(matches)
    except requests.RequestException as exc:
        with print_lock:
            print(f"{Fore.RED}Failed to fetch {url}: {exc}{Style.RESET_ALL}")
        return []


def format_proxies_for_requests(proxy_str, proxy_type_hint):

    ipport = proxy_str.strip()
    # automatically try HTTP/HTTPS by default
    if proxy_type_hint in ("http", "https", "auto"):
        return {"http": f"http://{ipport}", "https": f"http://{ipport}"}
    if proxy_type_hint == "socks4":
        return {"http": f"socks4://{ipport}", "https": f"socks4://{ipport}"}
    if proxy_type_hint == "socks5":
        return {"http": f"socks5://{ipport}", "https": f"socks5://{ipport}"}
    # fallback
    return {"http": f"http://{ipport}", "https": f"http://{ipport}"}


def test_proxy(proxy_str, session, test_url, timeout, proxy_type_hint, stop_event):

    if stop_event.is_set():
        return None

    proxies = format_proxies_for_requests(proxy_str, proxy_type_hint)
    try:

        resp = session.get(test_url, proxies=proxies, timeout=timeout)
        resp.raise_for_status()

        if resp.status_code == 200:
            return proxy_str
    except requests.RequestException:
        return None
    return None


def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Validated proxy fetcher and tester (optimized).")
    parser.add_argument("--type", choices=["http", "https", "socks4", "socks5", "mixed", "auto"],
                        default="mixed",
                        help="Proxy source/type to fetch/test (default: mixed). 'auto' will test as HTTP/HTTPS.")
    parser.add_argument("--count", type=int, default=10, help="How many working proxies to find/save.")
    parser.add_argument("--workers", type=int, default=50, help="Number of concurrent workers (threads).")
    parser.add_argument("--timeout", type=int, default=6, help="Per-proxy request timeout in seconds.")
    parser.add_argument("--test-url", type=str, default="https://www.example.com", help="URL to test through proxies.")
    parser.add_argument("--save", type=str, default="proxies.txt", help="Output filename to save found proxies.")
    parser.add_argument("--no-fetch", action="store_true", help="Skip fetching URLs; read from stdin instead.")
    args = parser.parse_args()

    desired = max(1, args.count)
    max_workers = max(1, min(200, args.workers))
    timeout = max(1, args.timeout)

    proxy_urls_map = {
        "http": [
            "https://api.openproxylist.xyz/http.txt",
            "https://rootjazz.com/proxies/proxies.txt",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"

        ],
        "https": [
            "https://www.sslproxies.org/",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt"
        ],
        "socks4": [
            "https://api.openproxylist.xyz/socks4.txt",
            "https://www.proxy-list.download/api/v1/get?type=socks4",
            "https://www.socks-proxy.net/",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=SOCKS4&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks4.txt"
        ],
        "socks5": [
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://api.openproxylist.xyz/socks5.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
            "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks5.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=SOCKS5&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
        ],
        "mixed": [
            'https://www.sslproxies.org/',
            'https://www.google-proxy.net/',
            'https://free-proxy-list.net/anonymous-proxy.html',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://www.us-proxy.org/',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=SOCKS4&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all',
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=SOCKS5&timeout=10000&country=all&ssl=all&anonymity=all",
            'https://free-proxy-list.net/'
        ]
    }


    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    chosen_type = args.type
    urls_to_fetch = []
    if chosen_type == "mixed":
        urls_to_fetch = proxy_urls_map["mixed"]
    elif chosen_type in proxy_urls_map:
        urls_to_fetch = proxy_urls_map[chosen_type]
    else:  
        urls_to_fetch = proxy_urls_map["mixed"]

    start_time = time.time()
    all_candidates = set()

    if args.no_fetch:

        print(f"{Fore.YELLOW}Reading proxy list from stdin... (end with Ctrl-D){Style.RESET_ALL}")
        for line in sys.stdin:
            m = IPPORT_RE.search(line)
            if m:
                all_candidates.add(m.group(0))
    else:
        with ThreadPoolExecutor(max_workers=min(len(urls_to_fetch), max_workers)) as fetch_pool:
            future_to_url = {fetch_pool.submit(fetch_proxies_from_url, url, session, timeout * 2): url
                             for url in urls_to_fetch}
            print(f"{Fore.WHITE}[~] {Fore.MAGENTA}Fetching Proxy lists...{Style.RESET_ALL}\n")
            for fut in as_completed(future_to_url):
                url = future_to_url[fut]
                try:
                    proxies = fut.result()
                    if proxies:
                        all_candidates.update(proxies)
                        with print_lock:
                            print(f"{Fore.WHITE}[+] {Fore.GREEN}Fetched {len(proxies)} proxies from: {Fore.WHITE}{url}{Style.RESET_ALL}")
                except Exception as exc:
                    with print_lock:
                        print(f"{Fore.RED}Error fetching from {url}: {exc}{Style.RESET_ALL}")

    if not all_candidates:
        print(f"{Fore.RED}No proxy candidates found. Exiting.{Style.RESET_ALL}")
        return


    stop_event = Event()
    found = set()
    found_lock = Lock()
    proxy_list = list(all_candidates)
    total_candidates = len(proxy_list)
    with print_lock:
        print(f"\n{Fore.WHITE}[~] {Fore.MAGENTA}Candidates collected: {Fore.WHITE}{total_candidates}. {Fore.YELLOW}Starting validation...{Style.RESET_ALL}\n")

    proxy_type_hint = chosen_type if chosen_type in ("http", "https", "socks4", "socks5") else "auto"


    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {
            executor.submit(test_proxy, p, session, args.test_url, timeout, proxy_type_hint, stop_event): p
            for p in proxy_list
        }

        try:
            for fut in as_completed(future_to_proxy):
                proxy = future_to_proxy[fut]
                result = fut.result()
                if result:
                    with found_lock:
                        if result not in found:
                            found.add(result)
                            with print_lock:
                                print(f"{Fore.CYAN}{result.ljust(24)} {Fore.WHITE}: {Fore.GREEN}[ACTIVE]{Style.RESET_ALL}")
                    if len(found) >= desired:
                        stop_event.set()

                        break

                if stop_event.is_set():
                    break
        except KeyboardInterrupt:
            with print_lock:
                print(f"\n{Fore.RED}Interrupted by user. Stopping...{Style.RESET_ALL}")
            stop_event.set()

    # Finalize and save
    elapsed = time.time() - start_time
    found_list = sorted(found)
    with print_lock:
        print(f"\n{Fore.WHITE}[~] {Fore.MAGENTA}Found {Fore.GREEN}{len(found_list)} {Fore.WHITE}working proxies in {Fore.CYAN}{elapsed:.2f}s{Style.RESET_ALL}\n")

    if found_list:
        save_path = os.path.abspath(args.save)
        try:
            with open(save_path, "w") as fh:
                fh.write("\n".join(found_list) + "\n")
            print(f"{Fore.WHITE}[~] {Fore.MAGENTA}Saved to: {Fore.WHITE}{save_path}{Style.RESET_ALL}\n")
        except OSError as exc:
            print(f"{Fore.RED}Failed to save file: {exc}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No working proxies found.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
