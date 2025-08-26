import subprocess

def wmi_exec(target_ip, domain, username, password, command):
    print(f"\n[+] Executing command on {target_ip} via WMI...")
    
    credentials = f"{domain}/{username}:{password}@{target_ip}"
    
    # We need to pass the command to wmiexec
    full_command = [
        "impacket-wmiexec",
        credentials,
        command
    ]

    print(f"[*] Running: {' '.join(full_command)}")

    try:
        # We don't need to check for output here, just whether it succeeded.
        # We'll run this in the background. For a real shell, we'd need a different approach.
        result = subprocess.run(full_command, capture_output=True, text=True, check=True)
        print("[+] Command executed successfully.")
        print("[*] Output:")
        print(result.stdout)
        return True
    except FileNotFoundError:
        print("\n[!] ERROR: 'impacket-wmiexec' not found.")
        print("[!] Please ensure impacket is installed and in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print("\n[!] ERROR: WMI execution failed. Check credentials and permissions.")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        return False