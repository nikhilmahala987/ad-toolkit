import os
import sys
from datetime import datetime
from modules import enumeration
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    print("="*60)
    print("       Python Active Directory Post-Exploitation Toolkit")
    print("="*60)
    print()

def display_menu():
    """Displays the main menu options."""
    print("Main Menu:")
    print("  1. Enumeration")
    print("  2. Credential Access")
    print("  3. Lateral Movement")
    print("  4. Privilege Escalation")
    print("  5. Persistence")
    print("  6. Defense Evasion & OPSEC")
    print("  7. Exit")
    print()

def main():
    """Main function to run the toolkit."""
    while True:
        clear_screen()
        display_banner()
        display_menu()

        choice = input("Enter your choice [1-7]: ")

        if choice == '1':
            print("Executing Enumeration module...")
            enumeration.run()
            input("Press Enter to continue...")
        elif choice == '2':
            print("Executing Credential Access module...")
            # placeholder: credential_access.run()
            input("Press Enter to continue...")
        elif choice == '3':
            print("Executing Lateral Movement module...")
            # placeholder: lateral_movement.run()
            input("Press Enter to continue...")
        elif choice == '4':
            print("Executing Privilege Escalation module...")
            # placeholder: priv_esc.run()
            input("Press Enter to continue...")
        elif choice == '5':
            print("Executing Persistence module...")
            # placeholder: persistence.run()
            input("Press Enter to continue...")
        elif choice == '6':
            print("Executing Defense Evasion & OPSEC module...")
            # placeholder: opsec.run()
            input("Press Enter to continue...")
        elif choice == '7':
            print("Exiting toolkit. Stay safe.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()