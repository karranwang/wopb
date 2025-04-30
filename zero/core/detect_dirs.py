import requests
from concurrent.futures import ThreadPoolExecutor

def load_paths(path="dirs.txt"):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File wordlist tidak ditemukan: {path}")
        return []

def check_path(target, path):
    url = f"{target.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code in [200, 301, 302, 403]:
            print(f"[+] Ditemukan path: {url} (Status: {response.status_code})")
    except requests.exceptions.RequestException:
        print(f"[!] Error mengakses {url}")

def scan_paths(target, wordlist_path="dirs.txt", threads=10):
    print(f"[*] Memulai pemindaian direktori pada {target}")
    paths = load_paths(wordlist_path)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for path in paths:
            executor.submit(check_path, target, path)

    print("[*] Selesai scan direktori.")
