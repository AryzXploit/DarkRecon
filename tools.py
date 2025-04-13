import json
import subprocess
from rich.console import Console
import os
import requests
import re  # <-- Tambahin ini

console = Console()

# Path ke file user-role
SECRET_DIR = os.path.expanduser("~/.config/.hidden_directory/")
SECRET_FILE = os.path.join(SECRET_DIR, "hidden_users.json")

# Ganti webhook lu kalau belum
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1360660554968076298/b7bs6DF1kQBpA9aoyLgOEbxEmCJ2bdlLM_m4loXP2SCUehFzBI3KFKe5lwrfTozlfxsY"

# --- Load user dari file ---
def load_users():
    try:
        with open(SECRET_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}}

def check_user_role(user_id):
    users = load_users()
    return users["users"].get(user_id, {}).get("role", "free")

# --- Kirim hasil ke Discord ---
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def send_to_discord(result, tool_name, url):
    if not DISCORD_WEBHOOK or "discord.com/api/webhooks/" not in DISCORD_WEBHOOK:
        console.print("❌ [bold red]Webhook Discord belum di-setup atau salah![/]")
        return

    try:
        cleaned_result = result.strip()
        if not cleaned_result:
            return

        # Potong output kalau terlalu panjang
        max_length = 1900
        if len(cleaned_result) > max_length:
            cleaned_result = cleaned_result[:max_length] + "\n... [output truncated]"

        payload = {
            "embeds": [
                {
                    "title": f"🛠️ Tool: {tool_name}",
                    "description": f"🌐 **Target:** `{url}`\n```\n{cleaned_result}\n```",
                    "color": 5814783
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)

        if response.status_code not in [200, 204]:
            console.print(f"⚠️ [bold yellow]Gagal kirim ke Discord. Status: {response.status_code}, Resp: {response.text}[/bold yellow]")

    except Exception as e:
        console.print(f"❌ [bold red]Error kirim webhook:[/] {e}")

# --- Jalankan tools ---
def run_command(command, tool_name=None, url=None):
    try:
        console.print(f"\n⚡ [bold cyan]Running: {command}[/bold cyan]\n")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and stderr:
            return f"❌ [bold red]Error:[/] {stderr}"

        filtered_output = "\n".join([
            line for line in stdout.splitlines()
            if not any(ignore in line for ignore in ["INF]", "WRN]", "projectdiscovery.io"])
        ]).strip()

        output_to_send = filtered_output if filtered_output else stdout
        output_to_send = strip_ansi_codes(output_to_send)

        # Flag biar gak kekirim dua kali
        sent_to_discord = False

        if output_to_send and tool_name and url and not sent_to_discord:
            send_to_discord(output_to_send, tool_name, url)
            sent_to_discord = True

        return output_to_send if output_to_send else "⚠️ [bold yellow]No output or no relevant result returned![/bold yellow]"

    except Exception as e:
        return f"❌ [bold red]Exception saat eksekusi:[/] {e}"

# ✅ TOOLS GRATIS
def whatweb_scan(url): return run_command(f"whatweb {url}", "WhatWeb", url)
def sqlmap_scan(url): return run_command(f"sqlmap -u {url} --random-agent --batch --dbs --level 3 --tamper=between,space2comment --hex --delay 5", "SQLMap", url)
def nuclei_exposed_panel(url): return run_command(f"nuclei -u {url} -t exposures -silent", "Nuclei Panel", url)
def nmap_scan(target): return run_command(f"nmap -sV {target}", "Nmap", target)
def gobuster_scan(url, wordlist): return run_command(f"gobuster dir -u {url} -w {wordlist}", "Gobuster", url)
def dns_tools(domain): return run_command(f"dig {domain}", "Dig", domain)
def nslookup(domain): return run_command(f"nslookup {domain}", "NSLookup", domain)
def subzy(domain): return run_command(f"subzy run --target {domain}", "Subzy", domain)

# 🔒 TOOLS PREMIUM
def subrecon_scan(domain, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"SubRecon -d {domain}", "SubRecon", domain)
    return "🔒 Access Denied!"

def wpscan(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"wpscan --url {url} --enumerate vp,vt,u --random-user-agent", "WPScan", url)
    return "🔒 Access Denied!"

def dalfox_scan(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"dalfox url {url}", "Dalfox", url)
    return "🔒 Access Denied!"

def nuclei_email_extraction(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"nuclei -u {url} -tags exposures -silent", "Nuclei Email Extraction", url)
    return "🔒 Access Denied!"

def nuclei_technologies(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"nuclei -u {url} -tags technologies -silent", "Nuclei Technologies", url)
    return "🔒 Access Denied!"

def nuclei_rce_scan(url, user_id):
    if check_user_role(user_id) in ["premium", "admin"]:
        return run_command(f"nuclei -u {url} -tags rce -silent", "Nuclei RCE", url)
    return "🔒 Access Denied!"
