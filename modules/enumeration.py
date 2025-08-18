import subprocess
import shlex

def run():
    while True:
        print("\n--- Enumeration & Situational Awareness ---")
        print("1. Enumerate Domain Users (LDAP)")
        print("2. Enumerate Domain Groups")
        print("3. (Coming Soon) Find Domain Controllers")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            target_ip = input("Enter Target IP (Domain Controller): ")
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            enumerate_users(target_ip, domain, username, password)
        elif choice == '2':
            target_ip = input("Enter Target IP (Domain Controller): ")
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            enumerate_groups(target_ip, domain, username, password)
        elif choice == '99':
            print("Returning to main menu...")
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def enumerate_users(target_ip, domain, username, password):
    print("\nEnumerating domain users via LDAP...")
    # Format for ldapsearch: domain/username:password@target_ip
    credentials = f"{domain}/{username}:{password}"
    base_dn = f"DC={domain.replace('.',',DC=')}"

    # Using shlex.split to handle command-line arguments safely
    command = [
        "impacket-ldapsearch",
        "-dc-ip", target_ip,
        credentials,
        "-base", base_dn,
        "(objectClass=user)",
        "sAMAccountName"
    ]

    print(f"[*] Running command: {' '.join(command)}")
    
    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print("\nCommand executed successfully. Output:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)

    except FileNotFoundError:
        print("\n[!] ERROR: 'impacket-ldapsearch' not found.")
        print("[!] Please ensure impacket is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print("\n[!] ERROR: Command failed.")
        print(f"[!] Return Code: {e.returncode}")
        print("[!] Stderr:")
        print(e.stderr)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

    input("\nPress Enter to continue...")

def enumerate_groups(target_ip, domain, username, password):
    print("\n[+] Enumerating domain groups via LDAP...")
    credentials = f"{domain}/{username}:{password}"
    base_dn = f"DC={domain.replace('.',',DC=')}"
    
    command = [
        "impacket-ldapsearch",
        "-dc-ip", target_ip,
        credentials,
        "-base", base_dn,
        "(objectClass=group)",
        "cn"
    ]

    print(f"[*] Running command: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("\n[+] Command executed successfully. Output:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)
    except FileNotFoundError:
        print("\n[!] ERROR: 'impacket-ldapsearch' not found.")
        print("[!] Please ensure impacket is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print("\n[!] ERROR: Command failed.")
        print(f"[!] Return Code: {e.returncode}")
        print("[!] Stderr:")
        print(e.stderr)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

    input("\nPress Enter to continue...")