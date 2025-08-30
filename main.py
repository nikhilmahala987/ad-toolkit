import os
import sys
from datetime import datetime
from modules import enumeration, credential_access, lateral_movement

def main_menu():
    while True:
        print("\n--- Python AD Toolkit ---")
        print("Select a module to continue:")
        print("1. Enumeration & Situational Awareness")
        print("2. Credential Access")
        print("3. Lateral Movement")
        print("4. Privilege Escalation (Not Implemented)")
        print("5. Persistence (Not Implemented)")
        print("6. OPSEC & Defense Evasion (Not Implemented)")
        print("99. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            enumeration.run()
        elif choice == '2':
            credential_access.run()
        elif choice == '3':
            lateral_movement.run()
        elif choice == '99':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
