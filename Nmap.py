import subprocess
from prettytable import PrettyTable
from colorama import Fore, Style, init
from tqdm import tqdm
import time
import pyfiglet

# Inisialisasi colorama
init(autoreset=True)

def run_nmap_scan(target, scan_type):
    """
    Menjalankan scan Nmap berdasarkan target dan tipe scan yang dipilih pengguna.
    
    Parameters:
    target (str): Alamat IP atau domain yang ingin discan.
    scan_type (str): Tipe scan yang dipilih pengguna.
    
    Returns:
    str: Output hasil scan Nmap.
    """
    command = ['nmap', '-v'] + scan_type.split() + [target]
    
    # Menampilkan progress bar selama scanning
    print("\nMemulai scanning...")
    with tqdm(total=100, desc="Proses Scanning", ncols=80, dynamic_ncols=True, ascii=True) as pbar:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
            time.sleep(0.1)
            pbar.update(0.5)  # Memperbarui bar secara bertahap
        output, error = process.communicate()

    if process.returncode == 0:
        return output.decode('utf-8')
    else:
        return f"Terjadi kesalahan:\n{error.decode('utf-8')}"

def main():
    while True:
        # Membuat margin atas
        print("\n" * 3)

        # Membuat header dengan pyfiglet
        header = pyfiglet.figlet_format("nmap auto", font="slant")
        subheader = "coded by D A N Z"
        
        # Menampilkan header dengan warna
        print(Fore.CYAN + Style.BRIGHT + header)
        print(Fore.MAGENTA + subheader.center(80))
        print("\n")
        
        # Tabel untuk input IP/URL
        table = PrettyTable()
        table.field_names = ["Input"]
        table.add_row(["Masukkan URL/IP Address: "])
        print(table)
        
        # Input URL/IP dari user
        target = input(">> ")

        # List metode scanning tanpa hak akses root
        non_root_scan_options = {
            "1": "-sT -v (TCP connect scan)",
            "2": "-sV -v (Version detection)",
            "3": "-Pn -v (No ping before scan)",
            "4": "-sC -v (Script scan)"
        }
        
        # List metode scanning yang memerlukan hak akses root
        root_scan_options = {
            "5": "-sS -v (TCP SYN scan)",
            "6": "-sU -v (UDP scan)",
            "7": "-O -v (OS detection)",
            "8": "-A -v (Aggressive scan, includes -O, -sV and more)",
            "9": "Idle Scan",
            "10": "Decoy Scan"
        }

        print("\nPilih metode scanning yang tersedia:")
        
        # Tabel untuk memilih metode scanning tanpa hak akses root
        non_root_table = PrettyTable()
        non_root_table.field_names = ["No.", "Scan Type", "Description"]
        for key, value in non_root_scan_options.items():
            non_root_table.add_row([key, value.split()[0], value.split(' ', 1)[1]])
        print("Metode scan tanpa hak akses root:")
        print(non_root_table)

        # Tabel untuk memilih metode scanning yang memerlukan hak akses root
        root_table = PrettyTable()
        root_table.field_names = ["No.", "Scan Type", "Description"]
        for key, value in root_scan_options.items():
            root_table.add_row([key, value.split()[0], value.split(' ', 1)[1]])
        print("Metode scan dengan hak akses root:")
        print(root_table)
        
        # Meminta input metode scanning dari user
        choice = input("Masukkan nomor pilihan metode scanning: ")

        if choice in non_root_scan_options:
            scan_type = non_root_scan_options[choice]
        elif choice in root_scan_options:
            if choice == "9":  # Idle Scan
                zombie_ip = input("Masukkan Zombie IP untuk Idle Scan: ")
                scan_type = f"-sI {zombie_ip} -v"
            elif choice == "10":  # Decoy Scan
                decoy_choice = input("Ingin menggunakan jumlah decoy (1) atau memasukkan IP decoy manual (2)? ")
                if decoy_choice == "1":
                    num_decoys = input("Masukkan jumlah decoy yang diinginkan: ")
                    scan_type = f"-D RND:{num_decoys} -v"
                elif decoy_choice == "2":
                    decoy_ips = input("Masukkan IP decoy secara manual (pisahkan dengan koma): ")
                    scan_type = f"-D {decoy_ips} -v"
                else:
                    print(Fore.RED + "Pilihan tidak valid, menggunakan scan default (-sS -v)")
                    scan_type = "-sS -v"
            else:
                scan_type = root_scan_options[choice]
        else:
            print(Fore.RED + "Pilihan tidak valid, menggunakan scan default (-sS -v)")
            scan_type = "-sS -v"

        # Menjalankan scan
        hasil_scan = run_nmap_scan(target, scan_type)
        
        # Menampilkan hasil scan
        print("\n===== Hasil Scan =====")
        print(hasil_scan)

        # Opsi untuk melakukan scan kembali
        retry = input("\nApakah ingin melakukan scan kembali? (y/n): ").strip().lower()
        if retry != 'y':
            break

if __name__ == "__main__":
    main()
