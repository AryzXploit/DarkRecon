import subprocess
from rich.console import Console
import os
import json  # Import the json module

console = Console()

# Fungsi untuk menjalankan perintah
def run_command(command):
    try:
        console.print(f"\n⚡ [bold cyan]Running: {command}[/bold cyan]\n")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stderr:
            return f"❌ [bold red]Real Error:[/] {stderr}"
        
        if not stdout:
            return "⚠️ [bold yellow]No vulnerabilities found or no output returned![/bold yellow]"
        
        filtered_output = "\n".join([
            line for line in stdout.splitlines()
            if not any(ignore in line for ignore in ["INF]", "WRN]", "projectdiscovery.io"])
        ]).strip()

        if filtered_output:
            return filtered_output
        else:
            return "⚠️ [bold yellow]No relevant output received from the command![/bold yellow]"
    except Exception as e:
        return f"❌ [bold red]Exception:[/] {e}"

# ✅ FREE TOOLS
def whatweb_scan(url):
    return run_command(f"whatweb {url}")

def sqlmap_scan(url):
    return run_command(f"sqlmap -u {url} --batch --dbs")

def nuclei_exposed_panel(url):
    return run_command(f"nuclei -u {url} -t /home/user/nuclei-templates/http/exposed-panels/ -silent")

def nmap_scan(target):
    return run_command(f"nmap -sV {target}")

def gobuster_scan(url, wordlist):
    return run_command(f"gobuster dir -u {url} -w {wordlist}")

def dns_tools(domain):
    return run_command(f"dig {domain}")

def nslookup(domain):
    return run_command(f"nslookup {domain}")

# 🔒 PREMIUM TOOLS
def subrecon_scan(domain, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"subfinder -d {domain} -all")
    return "🔒 Access Denied!"

def wpscan(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"wpscan --url {url} --enumerate vp,vt,u")
    return "🔒 Access Denied!"

def dalfox_scan(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"dalfox url {url}")
    return "🔒 Access Denied!"

def nuclei_email_extraction(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"nuclei -u {url} -t /home/user/nuclei-templates/http/exposures/ -silent")
    return "🔒 Access Denied!"

def nuclei_technologies(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"nuclei -u {url} -t /home/user/nuclei-templates/technologies/ -silent")
    return "🔒 Access Denied!"

# Fungsi cek role (bisa diimplementasikan dengan file JSON atau lainnya)
def check_user_role(user_id):
    try:
        with open(os.path.expanduser("~/.config/.hidden_directory/hidden_users.json"), "r") as file:
            data = json.load(file)
        if user_id in data["users"]:
            return data["users"][user_id]["role"]
        else:
            return "none"
    except (FileNotFoundError, json.JSONDecodeError):
        return "none"
