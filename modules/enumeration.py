import subprocess
import shlex

try:
    import dns.resolver
except ImportError:
    print("[!] Module 'dnspython' not found. Please run 'pip install -r requirements.txt'")
    exit()

def find_dc_ip(domain):
    """
    Finds the IP address of a domain controller using DNS SRV records.
    """
    print(f"\n[+] Attempting to find a Domain Controller for '{domain}'...")
    srv_record = f'_ldap._tcp.dc._msdcs.{domain}'
    try:
        # Resolve the SRV record
        answers = dns.resolver.resolve(srv_record, 'SRV')
        if not answers:
            print("[!] No SRV records found.")
            return None
        
        # Take the first record and get the hostname
        hostname = str(answers[0].target).rstrip('.')
        print(f"[*] Found DC hostname: {hostname}")

        # Resolve the hostname to an IP address (A record)
        ip_answers = dns.resolver.resolve(hostname, 'A')
        if not ip_answers:
            print(f"[!] Could not resolve hostname '{hostname}' to an IP.")
            return None
            
        dc_ip = str(ip_answers[0])
        print(f"[+] Resolved DC IP: {dc_ip}")
        return dc_ip

    except dns.resolver.NXDOMAIN:
        print(f"[!] Error: The domain '{domain}' does not exist or could not be queried.")
        return None
    except dns.resolver.NoAnswer:
        print(f"[!] Error: No SRV record found for '{srv_record}'. Is this a valid AD domain?")
        return None
    except Exception as e:
        print(f"[!] An unexpected DNS error occurred: {e}")
        return None

def run():
    while True:
        print("\n--- Enumeration & Situational Awareness ---")
        print("1. Find Domain Controller")
        print("2. Enumerate Domain Users (LDAP)")
        print("3. Enumerate Domain Groups (LDAP)")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            find_dc_ip(domain)
            input("\nPress Enter to continue...")
        elif choice == '2' or choice == '3':
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            target_ip = find_dc_ip(domain)
            if not target_ip:
                print("[!] Could not proceed without a Domain Controller IP.")
                input("\nPress Enter to continue...")
                continue
            
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            
            if choice == '2':
                enumerate_users(target_ip, domain, username, password)
            else:
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
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print("\nCommand executed successfully. Output:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)
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

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("\n[+] Command executed successfully. Output:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
    input("\nPress Enter to continue...")