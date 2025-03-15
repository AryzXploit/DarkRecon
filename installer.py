import os
import subprocess
import json

def install_requirements():
    print("[*] Installing dependencies...")
    try:
        subprocess.check_call(['pip', 'install', 'rich', '--break-system-packages'])
    except subprocess.CalledProcessError:
        print("[!] Failed to install dependencies. Please install them manually.")
        return False
    print("[+] Dependencies installed successfully.")
    return True

def setup_hidden_directory():
    print("[*] Setting up hidden directory for user data...")
    hidden_dir = os.path.expanduser("~/.config/.hidden_directory/")
    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir, exist_ok=True)
        
    users_file = os.path.join(hidden_dir, "hidden_users.json")
    if not os.path.exists(users_file):
        with open(users_file, "w") as file:
            file.write('{"users": {}}')
    print("[+] Hidden directory and user file created successfully.")

def create_shortcut():
    print("[*] Creating shortcut command 'darkrecon'...")
    try:
        script_path = os.path.abspath("darkrecon.py")
        bash_alias = os.path.expanduser("~/.bashrc")
        zsh_alias = os.path.expanduser("~/.zshrc")

        alias_command = f"alias darkrecon='python3 {script_path}'\n"

        if os.path.exists(bash_alias):
            with open(bash_alias, "a") as file:
                file.write(alias_command)
            print("[+] Shortcut added to ~/.bashrc. Use 'source ~/.bashrc' to apply.")

        if os.path.exists(zsh_alias):
            with open(zsh_alias, "a") as file:
                file.write(alias_command)
            print("[+] Shortcut added to ~/.zshrc. Use 'source ~/.zshrc' to apply.")

    except Exception as e:
        print(f"[!] Failed to create shortcut: {e}")

def main():
    print("==== DarkRecon Installer ====")

    if install_requirements():
        setup_hidden_directory()
        create_shortcut()
        print("[+] Installation completed successfully.")
    else:
        print("[!] Installation failed.")

if __name__ == "__main__":
    main()
