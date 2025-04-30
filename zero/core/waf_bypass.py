# core/waf_bypass.py

import requests

def waf_bypass_test(target):
    print(f'[+] Menguji bypass WAF dari {target}\n')

    if not target.startswith("http"):
        target = "http://" + target
    if target.endswith("/"):
        target = target[:-1]

    payloads = [
        "/wp-login.php",                     # Normal
        "/wp-login.php?",                    # Tambahan ?
        "/wp-login.php/.",                   # Tambahan ./
        "/wp-login.php/%20",                 # Space encoded
        "/wp-login.php..;/",                 # Dot trick
        "/%2e/wp-login.php",                 # Double encode
        "/wp-login.php?user=admin",          # Parameter aneh
        "/wp-login.php?redirect_to=//evil.com"  # Redirect test
    ]

    headers = {
        "User-Agent": "WPBF-Bypass/1.0"
    }

    for payload in payloads:
        url = target + payload
        try:
            res = requests.get(url, headers=headers, timeout=5)
            status = res.status_code
            print(f"[>] Coba: {url} => Status: {status}")
        except requests.RequestException as e:
            print(f"[-] Gagal mengakses: {url} ({e})")
    
    print("\n[!] Analisis manual disarankan untuk menilai apakah WAF berhasil dibypass.")
