# core/detect_users.py

import requests
import re

def enumerate_users(target):
    print(f'[+] Mendeteksi username dari {target}\n')

    # Normalisasi URL
    if not target.startswith("http"):
        target = "http://" + target
    if target.endswith("/"):
        target = target[:-1]

    found_users = set()

    # === Metode 1: ?author=1 dst. ===
    print("[*] Mencoba enumerasi menggunakan metode ?author=")
    for i in range(1, 11):
        url = f"{target}/?author={i}"
        try:
            res = requests.get(url, timeout=5, allow_redirects=True)
            if res.status_code == 200:
                match = re.search(r"/author/([^/]+)/", res.url)
                if match:
                    username = match.group(1)
                    if username not in found_users:
                        found_users.add(username)
                        print(f"  [+] Ditemukan: {username}")
        except requests.RequestException:
            pass

    # === Metode 2: REST API ===
    print("\n[*] Mencoba enumerasi menggunakan REST API /wp-json/wp/v2/users")
    try:
        api_url = f"{target}/wp-json/wp/v2/users"
        res = requests.get(api_url, timeout=5)
        if res.status_code == 200 and res.headers.get('Content-Type', '').startswith("application/json"):
            users = res.json()
            for user in users:
                username = user.get("slug")
                if username and username not in found_users:
                    found_users.add(username)
                    print(f"  [+] Ditemukan: {username}")
    except requests.RequestException:
        print("  [-] Gagal mengakses REST API")

    if not found_users:
        print("\n[-] Tidak ditemukan username.")
    else:
        print(f"\n[✓] Total username ditemukan: {len(found_users)}")
