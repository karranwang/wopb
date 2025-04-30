import os
import subprocess
from pyfiglet import figlet_format

from core.banner import banner
from core.menu import menu
from core.detect_version import detect_wp_version
from core.detect_plugins import detect_plugins
from core.detect_users import enumerate_users
from core.detect_dirs import scan_paths
from core.brute_force import brute_force_login
from core.brute_force_mass import brute_force_mass
from core.waf_detect import detect_waf
from core.waf_bypass import waf_bypass_test

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_from_github():
    print("[*] Mengecek pembaruan dari GitHub...")
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("[+] Update selesai!")
        else:
            print("[-] Gagal melakukan update.")
            print(result.stderr)
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    while True:
        clear()
        print(figlet_format("WPBF", font="slant"))
        banner()
        menu()
        choice = input("\nPilih menu > ")

        if choice == "1":
            target = input("Masukkan URL target: ")
            detect_wp_version(target)
        elif choice == "2":
            target = input("Masukkan URL target: ")
            detect_plugins(target)
        elif choice == "3":
            target = input("Masukkan URL target: ")
            enumerate_users(target)
        elif choice == "4":
            target = input("Masukkan URL target: ")
            scan_paths(target)
        elif choice == "5":
            target = input("Masukkan URL target: ")
            username = input("Masukkan username (atau tekan enter jika tidak tahu): ")
            brute_force_login(target, user=username if username else None)
        elif choice == "6":
            user = input("Masukkan username target (atau tekan enter jika tidak tahu): ")
            brute_force_mass(user=user if user else None)
        elif choice == "7":
            target = input("Masukkan URL target: ")
            detect_waf(target)
        elif choice == "8":
            target = input("Masukkan URL target: ")
            waf_bypass_test(target)
        elif choice == "9":
            update_from_github()
        elif choice == "0":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid.")

        input("\nTekan Enter untuk kembali ke menu...")
