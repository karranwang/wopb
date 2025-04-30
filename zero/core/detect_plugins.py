import requests
from concurrent.futures import ThreadPoolExecutor

def load_plugins(wordlist="plugins.txt"):
    try:
        with open(wordlist, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File tidak ditemukan: {wordlist}")
        return []

def check_plugin(target, plugin):
    url = f"{target.rstrip('/')}/wp-content/plugins/{plugin}/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code in [200, 301, 302, 403]:
            print(f"[+] Plugin ditemukan: {plugin} (Status: {response.status_code})")
    except requests.exceptions.RequestException:
        print(f"[!] Gagal mengakses {url}")

def detect_plugins(target, wordlist="plugins.txt", threads=10):
    print(f"[*] Memulai deteksi plugin pada: {target}")
    plugin_list = load_plugins(wordlist)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for plugin in plugin_list:
            executor.submit(check_plugin, target, plugin)

    print("[*] Selesai deteksi plugin.")
