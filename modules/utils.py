import random
import requests
import os

def save_result(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as f:
        f.write(content + "\n")

def load_proxies(proxy_file):
    proxies = []
    if proxy_file:
        try:
            with open(proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Proxy file '{proxy_file}' not found!")
    return proxies

def get_random_proxy(proxies):
    if proxies:
        proxy = random.choice(proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    else:
        return None

def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Linux; Android 11)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)"
    ]
    return random.choice(user_agents)

def check_wordpress(url):
    try:
        headers = {
            "User-Agent": random_user_agent()
        }
        if not url.endswith('/wp-login.php'):
            url = url.rstrip('/') + '/wp-login.php'
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if "user_login" in response.text and "wp-submit" in response.text and response.status_code == 200:
            return True
        else:
            return False
    except:
        return False
