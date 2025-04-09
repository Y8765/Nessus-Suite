import requests
import random
import string
import re
import sys
import os
import time
import platform
import subprocess
import hashlib
from pathlib import Path
from tqdm import tqdm
import urllib3
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import filedialog

print("\033[94m" + """
   ███╗   ██╗███████╗███████╗███████╗██╗   ██╗███████╗    ███████╗██╗   ██╗██╗████████╗███████╗
   ████╗  ██║██╔════╝██╔════╝██╔════╝██║   ██║██╔════╝    ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
   ██╔██╗ ██║█████╗  ███████╗███████╗██║   ██║███████╗    ███████╗██║   ██║██║   ██║   █████╗  
   ██║╚██╗██║██╔══╝  ╚════██║╚════██║██║   ██║╚════██║    ██╔════╝██║   ██║██║   ██║   ██╔══╝  
   ██║ ╚████║███████╗███████║███████║╚██████╔╝███████║    ███████║╚██████╔╝██║   ██║   ███████╗
   ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝    ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝  
                                     ✡ ✡ ✡ ✡  By Yair Avramovitch ✡ ✡ ✡ ✡   
                                    https://linkedin.com/in/yair-avramovitch
""" + "\033[0m")

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to set Nessus paths based on OS
def set_nessus_paths():
    default_paths = {
        "Windows": {
            "nessuscli": r"C:\Program Files\Tenable\Nessus\nessuscli.exe",
            "nessusd": r"C:\Program Files\Tenable\Nessus\nessusd.exe"
        },
        "Linux": {
            "nessuscli": "/opt/nessus/sbin/nessuscli",
            "nessusd": "/opt/nessus/sbin/nessusd"
        },
        "Darwin": {
            "nessuscli": "/Library/Nessus/run/sbin/nessuscli",
            "nessusd": "/Library/Nessus/run/sbin/nessusd"
        }
    }
    system = platform.system()
    if system in default_paths:
        nessuscli_path = default_paths[system]["nessuscli"]
        nessusd_path = default_paths[system]["nessusd"]
        if Path(nessuscli_path).exists() and Path(nessusd_path).exists():
            print(f"Detected OS: {system} with valid Nessus paths")
            print(f"nessuscli: {nessuscli_path}")
            print(f"nessusd: {nessusd_path}")
            return nessuscli_path, nessusd_path, system
    print("Could not automatically detect valid Nessus paths.")
    print("Please select your OS to assume default paths:")
    print("1. Windows")
    print("2. Linux")
    print("3. macOS")
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            system = "Windows"
            nessuscli_path = default_paths[system]["nessuscli"]
            nessusd_path = default_paths[system]["nessusd"]
            print(f"Assuming default paths for Windows:")
            print(f"nessuscli: {nessuscli_path}")
            print(f"nessusd: {nessusd_path}")
            return nessuscli_path, nessusd_path, system
        elif choice == "2":
            system = "Linux"
            nessuscli_path = default_paths[system]["nessuscli"]
            nessusd_path = default_paths[system]["nessusd"]
            print(f"Assuming default paths for Linux:")
            print(f"nessuscli: {nessuscli_path}")
            print(f"nessusd: {nessusd_path}")
            return nessuscli_path, nessusd_path, system
        elif choice == "3":
            system = "Darwin"
            nessuscli_path = default_paths[system]["nessuscli"]
            nessusd_path = default_paths[system]["nessusd"]
            print(f"Assuming default paths for macOS:")
            print(f"nessuscli: {nessuscli_path}")
            print(f"nessusd: {nessusd_path}")
            return nessuscli_path, nessusd_path, system
        else:
            print("Invalid choice. Please try again.")

# Utility Functions
def generate_random_string(length, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_phone():
    return ''.join(random.choice(string.digits) for _ in range(10))

def get_mail():
    prefix_length = random.randint(5, 10)
    prefix = generate_random_string(prefix_length, chars=string.ascii_lowercase + string.digits)
    domain_length = random.randint(4, 8)
    domain_name = generate_random_string(domain_length, chars=string.ascii_lowercase)
    tlds = ['com', 'org', 'net', 'edu', 'co', 'io']
    tld = random.choice(tlds)
    return f"{prefix}@{domain_name}.{tld}"

def select_file(title="Select a File", filetypes=(("All files", "*.*"),)):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path if file_path else None

def generate_nessus_key(app_type="nessus"):
    random_first_name = generate_random_string(random.randint(5, 10))
    random_last_name = generate_random_string(random.randint(4, 8))
    random_phone = generate_random_phone()
    random_company = generate_random_string(random.randint(5, 10))
    email = get_mail()

    data = {
        "skipContactLookup": "true",
        "product": app_type,
        "first_name": random_first_name,
        "last_name": random_last_name,
        "email": email,
        "partnerId": "",
        "phone": random_phone,
        "title": "Test",
        "company": random_company,
        "companySize": "10-49",
        "pid": "",
        "utm_source": "",
        "utm_campaign": "",
        "utm_medium": "",
        "utm_content": "",
        "utm_promoter": "",
        "utm_term": "",
        "alert_email": "",
        "_mkto_trk": "",
        "mkt_tok": "",
        "lookbook": "",
        "gclid": "",
        "country": "US",
        "region": "",
        "zip": "",
        "apps": [app_type],
        "tempProductInterest": "Tenable Nessus " + ("Expert" if app_type == "expert" else "Professional"),
        "gtm": {"category": "Nessus " + ("Expert" if app_type == "expert" else "Pro") + " 7-Day Trial"},
        "queryParameters": "",
        "referrer": ""
    }

    url = 'https://www.tenable.com/evaluations/api/v2/trials'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            regex = r"\"code\":\"([A-Z0-9-]+)\""
            matches = re.search(regex, response.text)
            activation_code = matches.group(1)
            print(f"Generated Nessus {app_type.capitalize()} 7-Day Trial Key Successfully!")
            print(f"Email: {email}")
            print(f"Activation Code: {activation_code}")
            return email, activation_code
        except AttributeError:
            print("Failed to parse activation code. Response:", response.text)
            return None, None
    else:
        print(f"Request failed. Status code: {response.status_code}")
        print("Response:", response.text)
        return None, None

def generate_keys_menu():
    while True:
        print("\033[1m\033[94m\n=== Generate Keys Menu ===\033[0m")
        print("1. Generate Nessus Professional 7-Day Trial Key")
        print("2. Generate Nessus Expert 7-Day Trial Key")
        print("3. Back to Main Menu")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            email, activation_code = generate_nessus_key("nessus")
            if activation_code:
                print("Professional 7-Day Trial Key generated.")
            else:
                print("Key generation failed. Try again.")
        elif choice == "2":
            email, activation_code = generate_nessus_key("expert")
            if activation_code:
                print("Expert 7-Day Trial Key generated.")
            else:
                print("Key generation failed. Try again.")
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")

def check_latest_plugins_version():
    try:
        response = requests.get("https://plugins.nessus.org/v2/plugins.php", verify=False)
        if response.status_code == 200:
            timestamp = response.text.strip()
            print("Response from plugins.nessus.org:")
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d%H%M")
                readable_time = dt.strftime("%Y-%m-%d %H:%M")
                print(f"{timestamp} | {readable_time}")
            except ValueError as e:
                print(f"{timestamp} | Unable to convert timestamp: {e}")
            return timestamp
        else:
            print(f"Failed to fetch plugin set. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching plugin set: {e}")
        return None

def download_plugins_file():
    url = "https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u=4e2abfd83a40e2012ebf6537ade2f207&p=29a34e24fc12d3f5fdfbb1ae948972c6"
    desktop_path = Path.home() / "Desktop"
    file_path = desktop_path / "all-2.0.tar.gz"

    if file_path.exists():
        print(f"A file named 'all-2.0.tar.gz' already exists on the desktop.")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print("Download canceled. Returning to the main menu.")
            return

    try:
        print(f"Downloading plugins file to: {file_path}")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")
            start_time = time.time()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

            progress_bar.close()
            end_time = time.time()
            download_time = end_time - start_time
            download_speed = total_size / (1024 * 1024 * download_time)
            print(f"Download completed! Speed: {download_speed:.2f} MB/s")
        else:
            print(f"Failed to download plugins file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading plugins file: {e}")

def plugin_stuff_menu():
    while True:
        print("\033[1m\033[94m\n=== Plugin Stuff Menu ===\033[0m")
        print("1. Check Latest Plugins Version")
        print("2. Download Plugins File to Desktop")
        print("3. Back to Main Menu")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            check_latest_plugins_version()
        elif choice == "2":
            download_plugins_file()
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")

def user_management_menu():
    while True:
        print("\033[1m\033[94m\n=== User Management ===\033[0m")
        print("1. Add a New User")
        print("2. Change User Password")
        print("3. Delete a User")
        print("4. List All Users")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-5): ")

        if choice == "1":
            username = input("Enter the username to add: ")
            subprocess.run([NESSUSCLI_PATH, "adduser", username])
        elif choice == "2":
            username = input("Enter the username to change password: ")
            subprocess.run([NESSUSCLI_PATH, "chpasswd", username])
        elif choice == "3":
            username = input("Enter the username to delete: ")
            subprocess.run([NESSUSCLI_PATH, "rmuser", username])
        elif choice == "4":
            subprocess.run([NESSUSCLI_PATH, "lsuser"])
        elif choice == "5":
            break
        else:
            print("Invalid option. Please select a valid option.")

def plugin_management_menu():
    while True:
        print("\033[1m\033[94m\n=== Plugin Management ===\033[0m")
        print("1. Update Plugins")
        print("2. Update Plugins from a Specific File")
        print("3. Check Plugin Feed Status")
        print("4. Back to Main Menu")
        choice = input("Select an option (1-4): ")

        if choice == "1":
            subprocess.run([NESSUSCLI_PATH, "update"])
        elif choice == "2":
            plugin_file = select_file(title="Select Nessus Plugin File", filetypes=(("TAR files", "*.tar.gz"), ("All files", "*.*")))
            if plugin_file:
                print(f"Selected plugin file: {plugin_file}")
                subprocess.run([NESSUSCLI_PATH, "update", plugin_file])
            else:
                print("No file selected. Operation canceled.")
        elif choice == "3":
            subprocess.run([NESSUSCLI_PATH, "fetch", "--check"])
        elif choice == "4":
            break
        else:
            print("Invalid option. Please select a valid option.")

def service_management_menu(system):
    while True:
        print("\033[1m\033[94m\n=== Service Management ===\033[0m")
        print("1. Start Nessus Service")
        print("2. Stop Nessus Service")
        print("3. Restart Nessus Service")
        print("4. Check Nessus Service Status")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-5): ")

        if choice == "1":
            if system == "Windows":
                subprocess.run(["net", "start", "Tenable Nessus"])
            else:
                subprocess.run(["systemctl", "start", "nessusd"])
        elif choice == "2":
            if system == "Windows":
                subprocess.run(["net", "stop", "Tenable Nessus"])
            else:
                subprocess.run(["systemctl", "stop", "nessusd"])
        elif choice == "3":
            if system == "Windows":
                subprocess.run(["net", "stop", "Tenable Nessus"])
                subprocess.run(["net", "start", "Tenable Nessus"])
            else:
                subprocess.run(["systemctl", "restart", "nessusd"])
        elif choice == "4":
            if system == "Windows":
                subprocess.run(["sc", "query", "Tenable Nessus"])
            else:
                subprocess.run(["systemctl", "status", "nessusd"])
        elif choice == "5":
            break
        else:
            print("Invalid option. Please select a valid option.")

def license_management_menu():
    while True:
        print("\033[1m\033[94m\n=== License Management ===\033[0m")
        print("1. Register Nessus with Activation Code")
        print("2. Register Nessus with Offline License File")
        print("3. Generate challenge For Offline License")
        print("4. Check Installed License")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-5): ")

        if choice == "1":
            activation_code = input("Enter the activation code: ")
            subprocess.run([NESSUSCLI_PATH, "fetch", "--register", activation_code])
        elif choice == "2":
            activation_file = select_file(title="Select Nessus License File", filetypes=(("License files", "*.lic"), ("All files", "*.*")))
            if activation_file:
                print(f"Selected license file: {activation_file}")
                subprocess.run([NESSUSCLI_PATH, "fetch", "--register-offline", activation_file])
            else:
                print("No file selected. Operation canceled.")
        elif choice == "3":
            subprocess.run([NESSUSCLI_PATH, "fetch", "--challenge"])
        elif choice == "4":
            subprocess.run([NESSUSCLI_PATH, "fetch", "--code-in-use"])
        elif choice == "5":
            break
        else:
            print("Invalid option. Please select a valid option.")

def reset_and_reconfigure_menu():
    while True:
        print("\033[1m\033[94m\n=== Reset Configuration ===\033[0m")
        print("1. Reset Nessus Configuration")
        print("2. Back to Main Menu")
        choice = input("Select an option (1-2): ")

        if choice == "1":
            subprocess.run([NESSUSCLI_PATH, "fix", "--reset"])
        elif choice == "2":
            break
        else:
            print("Invalid option. Please select a valid option.")

def logs_and_diagnostics_menu(system):
    while True:
        print("\033[1m\033[94m\n=== Logs and Diagnostics ===\033[0m")
        print("1. View Nessus Logs")
        print("2. Check Nessus Version")
        print("3. Nessus System Information")
        print("4. Nessus System Events Logs")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-4): ")

        if choice == "1":
            if system == "Windows":
                log_path = r"C:\ProgramData\Tenable\Nessus\nessus\logs\nessusd.messages"
                if Path(log_path).exists():
                    with open(log_path, "r") as log_file:
                        print(log_file.read())
                else:
                    print(f"Log file not found at {log_path}")
            else:
                log_path = "/opt/nessus/var/nessus/logs/nessusd.messages"
                subprocess.run(["tail", "-f", log_path])
        elif choice == "2":
            subprocess.run([NESSUSCLI_PATH, "-v"])
        elif choice == "3":
            subprocess.run([NESSUSCLI_PATH, "info", "--scanner-health-stats"])
        elif choice == "4":
            subprocess.run([NESSUSCLI_PATH, "info", "--system-events"])
        elif choice == "5":
            break
        else:
            print("Invalid option. Please select a valid option.")

def network_configuration_menu():
    while True:
        print("\033[1m\033[94m\n=== Network Configuration ===\033[0m")
        print("1. Change Listening Port")
        print("2. Bind to a Specific IP Address")
        print("3. Back to Main Menu")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            port = input("Enter the new port number: ")
            subprocess.run([NESSUSCLI_PATH, "fix", "--set-port", port])
        elif choice == "2":
            ip_address = input("Enter the IP address to bind to: ")
            subprocess.run([NESSUSCLI_PATH, "fix", "--set-address", ip_address])
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select a valid option.")

def backup_and_restore_menu():
    while True:
        print("\033[1m\033[94m\n=== Backup and Restore ===\033[0m")
        print("1. Backup Nessus Configuration")
        print("2. Restore Nessus Configuration")
        print("3. Back to Main Menu")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            backup_file = select_file(title="Select Backup Destination", filetypes=(("Backup files", "*.bak"), ("All files", "*.*")))
            if backup_file:
                print(f"Selected backup file: {backup_file}")
                subprocess.run([NESSUSCLI_PATH, "backup", "--create", backup_file])
            else:
                print("No file selected. Operation canceled.")
        elif choice == "2":
            backup_file = select_file(title="Select Backup File to Restore", filetypes=(("Backup files", "*.bak"), ("All files", "*.*")))
            if backup_file:
                print(f"Selected backup file: {backup_file}")
                subprocess.run([NESSUSCLI_PATH, "backup", "--restore", backup_file])
            else:
                print("No file selected. Operation canceled.")
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select a valid option.")

def nessus_useful_commands_menu(system):
    while True:
        print("\033[1m\033[94m\n=== Nessus Useful Commands ===\n\033[4mRun The Script/Exe As Admin, Nessus Actions Requires Privileges\033[0m")
        print("1. User Management")
        print("2. Plugin Management")
        print("3. Service Management")
        print("4. License Management")
        print("5. Reset and Reconfigure")
        print("6. Logs and Diagnostics")
        print("7. Network Configuration")
        print("8. Backup and Restore")
        print("9. Back to Main Menu")
        choice = input("Select an option (1-9): ")

        if choice == "1":
            user_management_menu()
        elif choice == "2":
            plugin_management_menu()
        elif choice == "3":
            service_management_menu(system)
        elif choice == "4":
            license_management_menu()
        elif choice == "5":
            reset_and_reconfigure_menu()
        elif choice == "6":
            logs_and_diagnostics_menu(system)
        elif choice == "7":
            network_configuration_menu()
        elif choice == "8":
            backup_and_restore_menu()
        elif choice == "9":
            break
        else:
            print("Invalid option. Please select a valid option.")

def download_file(url, file_path, expected_sha256=None):
    if file_path.exists():
        overwrite = input(f"'{file_path.name}' already exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print(f"Skipping {file_path.name}.")
            return False
    try:
        print(f"Downloading {file_path.name}...")
        response = requests.get(url, stream=True, verify=False)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=file_path.name)
            start_time = time.time()
            
            hasher = hashlib.sha256()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        hasher.update(chunk)
                        progress_bar.update(len(chunk))
            
            progress_bar.close()
            end_time = time.time()
            download_time = end_time - start_time
            download_speed = total_size / (1024 * 1024 * download_time) if download_time > 0 else 0
            
            computed_sha256 = hasher.hexdigest()
            if expected_sha256:
                if computed_sha256.lower() == expected_sha256.lower():
                    print(f"SHA256 verification passed: {computed_sha256}")
                else:
                    print(f"SHA256 verification failed!")
                    print(f"Expected: {expected_sha256}")
                    print(f"Computed: {computed_sha256}")
                    os.remove(file_path)
                    return False
            
            print(f"Completed {file_path.name}! Speed: {download_speed:.2f} MB/s")
            return True
        else:
            print(f"Failed to download {file_path.name}. Status code: {response.status_code}")
            if response.status_code == 401:
                print("This file requires authentication. You may need to log in to Tenable’s site.")
            return False
    except Exception as e:
        print(f"Error downloading {file_path.name}: {e}")
        return False

def parse_tenable_files(data):
    files = []
    if "releases" in data:
        for key in data["releases"]:
            release_group = data["releases"][key]
            if not release_group:  # Skip empty 'latest' (e.g., ot-security)
                continue
            if isinstance(release_group, list):
                for file in release_group:
                    files.append({
                        "file": file["file"],
                        "size": file["size"],
                        "sha256": file["sha256"],
                        "file_url": file["file_url"],
                        "release_date": file.get("release_date", "N/A"),
                        "requires_auth": file.get("requires_auth", False)
                    })
            elif isinstance(release_group, dict):
                for subkey in release_group:
                    for file in release_group[subkey]:
                        files.append({
                            "file": file["file"],
                            "size": file["size"],
                            "sha256": file["sha256"],
                            "file_url": file["file_url"],
                            "release_date": file.get("release_date", "N/A"),
                            "requires_auth": file.get("requires_auth", False)
                        })
    return files

def download_other_tenable_products(system):
    download_dir = Path.home() / "Desktop"
    download_dir.mkdir(exist_ok=True)

    categories = [
        {"title": "Compliance & Audit Files", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/download-all-compliance-audit-files"},
        {"title": "Tenable Security Center", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/security-center"},
        {"title": "Tenable Core", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/tenable-appliance"},
        {"title": "Sensor Proxy", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/sensor-proxy"},
        {"title": "Tenable Nessus Agent", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/nessus-agents"},
        {"title": "Tenable Nessus Network Monitor", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/nessus-network-monitor"},
        {"title": "Tenable OT Security", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/ot-security"},
        {"title": "Tenable Cloud Security", "files_index_url": "https://www.tenable.com/downloads/api/v2/pages/cloud-security"}
    ]

    def display_file_info(file):
        size_bytes = int(file['size'])
        if size_bytes < 1024 * 1024:  # Less than 1 MB
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        print(f"\nFilename: {file['file']}")
        print(f"Size: {size_str}")
        print(f"Release Date: {file['release_date'].split('T')[0] if file['release_date'] != 'N/A' else 'N/A'}")
        print(f"SHA256: {file['sha256']}")
        print(f"URL: {file['file_url']}")
        print(f"Requires Authentication: {'Yes' if file['requires_auth'] else 'No'}")

    def download_tenable_pkg(file):
        file_path = download_dir / file["file"]
        if file_path.exists():
            print(f"File already exists at: {file_path}")
            overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != "y":
                print(f"Skipping download of {file['file']}.")
                return
        if download_file(file["file_url"], file_path, file["sha256"]):
            print(f"Download completed! File saved to: {file_path}")
        else:
            print(f"Download failed")

    while True:
        print("\033[1m\033[94m\n=== Download Other Tenable Products ===\033[0m")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category['title']}")
        print(f"{len(categories) + 1}. Back to Installers Menu")
        
        choice = input(f"Select a category (1-{len(categories) + 1}): ").strip()
        if choice == str(len(categories) + 1):
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                category = categories[idx]
                print(f"\nFetching files from {category['files_index_url']}...")
                try:
                    response = requests.get(category["files_index_url"], verify=False)
                    if response.status_code != 200:
                        print(f"Failed to fetch files. Status code: {response.status_code}")
                        continue
                    data = response.json()
                except Exception as e:
                    print(f"Error fetching files: {e}")
                    continue

                files = parse_tenable_files(data)
                if not files:
                    print("No files found for this category.")
                    continue

                while True:
                    print(f"\nAvailable files for {category['title']}:")
                    for i, file in enumerate(files, 1):
                        size_bytes = int(file['size'])
                        if size_bytes < 1024 * 1024:
                            size_str = f"{size_bytes / 1024:.1f} KB"
                        else:
                            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                        date = file['release_date'].split('T')[0] if file['release_date'] != 'N/A' else 'N/A'
                        auth = " (Requires Auth)" if file['requires_auth'] else ""
                        print(f"{i}. {file['file']} ({size_str}, Released: {date}){auth}")
                    print(f"{len(files) + 1}. Back")

                    file_choice = input(f"Select a file to download (1-{len(files) + 1}): ").strip()
                    if file_choice == str(len(files) + 1):
                        break
                    try:
                        f_idx = int(file_choice) - 1
                        if 0 <= f_idx < len(files):
                            file = files[f_idx]
                            display_file_info(file)
                            if input("Download this file? (y/n): ").strip().lower() == "y":
                                download_tenable_pkg(file)
                        else:
                            print("Invalid selection")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input. Please enter a number.")

def download_nessus_installers(system):
    api_url = "https://www.tenable.com/downloads/api/v2/pages/nessus"
    download_dir = Path.home() / "Desktop"
    download_dir.mkdir(exist_ok=True)
    
    print("\n=== Download Nessus Classic Installers ===")
    print(f"Fetching Nessus installer list from {api_url}...")
    
    try:
        response = requests.get(api_url, verify=False)
        if response.status_code != 200:
            print(f"Failed to fetch installer list. Status code: {response.status_code}")
            return
        
        data = response.json()
        packages = []
        for release in data["releases"]["latest"].values():
            if isinstance(release, list):
                packages.extend([pkg for pkg in release if "file_url" in pkg])
    except Exception as e:
        print(f"Error fetching installer list: {e}")
        return
    
    def filter_packages(system, arch):
        filtered = []
        for pkg in packages:
            pkg_os = pkg.get("os", "").lower()
            pkg_arch = pkg.get("arch", "").lower()
            pkg_file = pkg.get("file", "").lower()
            
            if system == "Windows":
                if "windows" not in pkg_os:
                    continue
                if "amd64" in arch or "x86_64" in arch:
                    if "x64" in pkg_file or "amd64" in pkg_file:
                        filtered.append(pkg)
                elif "i386" in arch or "i686" in arch:
                    if "win32" in pkg_file or "x86" in pkg_file:
                        filtered.append(pkg)
            elif system == "Linux":
                if "linux" not in pkg_os:
                    continue
                if "x86_64" in arch or "amd64" in arch:
                    if "x86_64" in pkg_file or "amd64" in pkg_file:
                        filtered.append(pkg)
                elif "aarch64" in arch or "arm64" in arch:
                    if "aarch64" in pkg_file or "arm64" in pkg_file:
                        filtered.append(pkg)
                elif "arm" in arch:
                    if "armhf" in pkg_file or "arm" in pkg_file:
                        filtered.append(pkg)
            elif system == "Darwin":
                if "macos" not in pkg_os:
                    continue
                filtered.append(pkg)
        return filtered

    arch = platform.machine().lower()
    filtered_packages = filter_packages(system, arch)
    
    def display_pkg_info(pkg):
        print(f"\nFilename: {pkg['file']}")
        print(f"Size: {int(pkg['size'])/1024/1024:.1f} MB")
        print(f"Release Date: {pkg['release_date'].split('T')[0]}")
        print(f"SHA256: {pkg['sha256']}")
        print(f"URL: {pkg['file_url']}")
    
    def download_pkg(pkg):
        file_path = download_dir / pkg["file"]
        if file_path.exists():
            print(f"File already exists at: {file_path}")
            overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != "y":
                print(f"Skipping download of {pkg['file']}.")
                return
        print(f"\nDownloading {pkg['file']}...")
        if download_file(pkg["file_url"], file_path, expected_sha256=pkg["sha256"]):
            print(f"Download completed! File saved to: {file_path}")
        else:
            print("Download failed")

    windows_pkgs = [pkg for pkg in packages if pkg.get("os", "").lower() == "windows"]
    linux_pkgs = [pkg for pkg in packages if pkg.get("os", "").lower() == "linux"]
    macos_pkgs = [pkg for pkg in packages if pkg.get("os", "").lower() == "macos"]

    def show_os_menu(os_name, os_pkgs):
        while True:
            print(f"\n=== {os_name} Installers ===")
            for i, pkg in enumerate(os_pkgs, 1):
                print(f"  {i}. {pkg['file']}")
            print(f"  {len(os_pkgs) + 1}. Back")
            
            choice = input(f"\nSelect {os_name} installer (1-{len(os_pkgs) + 1}): ").strip().lower()
            if choice == str(len(os_pkgs) + 1) or choice == "back":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(os_pkgs):
                    selected_pkg = os_pkgs[idx]
                    display_pkg_info(selected_pkg)
                    if input("Download this installer? (y/n): ").lower() == "y":
                        download_pkg(selected_pkg)
                else:
                    print("Invalid selection")
            except ValueError:
                print("Invalid input. Please enter a number or 'back'.")

    while True:
        print("\033[1m\033[94m\n=== Download Nessus Classic Installers ===\033[0m")
        print(f"Detected OS: {system} ({arch})")
        print("1. Auto-select best installer")
        print("2. Windows installers")
        print("3. Linux installers")
        print("4. macOS installers")
        print("5. Back to Main Menu")
        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            if not filtered_packages:
                print("No matching installers found for your system")
            else:
                best_pkg = filtered_packages[0]
                print("\nRecommended installer:")
                display_pkg_info(best_pkg)
                if input("Download this installer? (y/n): ").lower() == "y":
                    download_pkg(best_pkg)
        
        elif choice == "2":
            if not windows_pkgs:
                print("No Windows installers available.")
            else:
                show_os_menu("Windows", windows_pkgs)
        
        elif choice == "3":
            if not linux_pkgs:
                print("No Linux installers available.")
            else:
                show_os_menu("Linux", linux_pkgs)
        
        elif choice == "4":
            if not macos_pkgs:
                print("No macOS installers available.")
            else:
                show_os_menu("MacOS", macos_pkgs)
        
        elif choice == "5":
            break
        else:
            print("Invalid option")

def main_menu(system):
    while True:
        print("\033[1m\033[94m\n=== Nessus Suite Main Menu ===\033[0m")
        print("1. Generate Keys")
        print("2. Plugin Stuff")
        print("3. Nessus Useful Commands (Admin/Root Is Needed)")
        print("4. Download Nessus Installers")
        print("5. Download Other Tenable Products")
        print("6. Exit")
        choice = input("Select an option (1-6): ")

        if choice == "1":
            generate_keys_menu()
        elif choice == "2":
            plugin_stuff_menu()
        elif choice == "3":
            nessus_useful_commands_menu(system)
        elif choice == "4":
            download_nessus_installers(system)
        elif choice == "5":
            download_other_tenable_products(system)
        elif choice == "6":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option. Please select 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    NESSUSCLI_PATH, NESSUSD_PATH, SYSTEM = set_nessus_paths()
    main_menu(SYSTEM)