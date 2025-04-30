# core/detect_version.py

import requests
import re

def detect_wp_version(target):
    print(f'[+] Deteksi versi WordPress dari {target}\n')

    # Normalisasi URL
    if not target.startswith("http"):
        target = "http://" + target
    if target.endswith("/"):
        target = target[:-1]

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; WPBF/1.0)'
    }

    try:
        res = requests.get(target, headers=headers, timeout=5)
        if res.status_code == 200:
            # Coba deteksi dari meta tag
            version = re.search(r'<meta name="generator" content="WordPress (\d+\.\d+(\.\d+)*)"', res.text, re.I)
            if version:
                print(f"[✓] Versi WordPress terdeteksi: {version.group(1)}")
                return

        # Coba file readme.html
        readme_url = f"{target}/readme.html"
        res_readme = requests.get(readme_url, headers=headers, timeout=5)
        if res_readme.status_code == 200:
            match = re.search(r"Version (\d+\.\d+(\.\d+)*)", res_readme.text, re.I)
            if match:
                print(f"[✓] Versi WordPress terdeteksi dari readme.html: {match.group(1)}")
                return

        print("[-] Versi WordPress tidak dapat dideteksi.")
    except requests.RequestException as e:
        print(f"[-] Gagal mengakses target: {e}")
