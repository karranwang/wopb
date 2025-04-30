# core/waf_detect.py

import requests

def detect_waf(target):
    print(f'[+] Mendeteksi WAF dari {target}\n')

    if not target.startswith("http"):
        target = "http://" + target
    if target.endswith("/"):
        target = target[:-1]

    test_url = f"{target}/?=<script>alert(1)</script>"

    headers = {
        "User-Agent": "WPBF-Scanner/1.0"
    }

    try:
        response = requests.get(test_url, headers=headers, timeout=5)
        status = response.status_code
        print(f"[•] Status kode: {status}")

        waf_signatures = [
            "sucuri", "cloudflare", "aws", "akamai", "imperva", "barracuda", "citrix", "f5", "fortiguard", "radware"
        ]

        # Deteksi via header
        detected = False
        for header, value in response.headers.items():
            lower_value = value.lower()
            for sig in waf_signatures:
                if sig in lower_value:
                    print(f"[✓] Terdeteksi WAF: {sig.upper()} (via header {header})")
                    detected = True

        # Deteksi via status
        if status in [406, 403, 501, 999]:
            print("[✓] Kemungkinan WAF aktif berdasarkan status kode.")

        if not detected and status == 200:
            print("[-] Tidak ada tanda-tanda WAF yang jelas terdeteksi.")
    except requests.RequestException as e:
        print(f"[-] Gagal mengakses target: {e}")
