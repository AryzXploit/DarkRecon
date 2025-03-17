from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from tools import *
import os
import time
import json  

console = Console()

def banner(role_status):
    status_text = "[bold green]Premium Access[/bold green]" if role_status == "premium" else "[bold yellow]Free Access[/bold yellow]"
    console.print(Panel(
        f"💀 [bold magenta]DarkRecon[/bold magenta] 💀\n"
        f"🛡️ [cyan]Advanced Security Testing Framework[/cyan]\n"
        f"👨‍💻 [bold white]Creator:[/] AryzXploit\n"
        f"🆙 [bold white]Version:[/] 1.1\n"  
        f"🆓 [bold white]Status:[/] {status_text}",
        expand=False,
        border_style="bright_magenta"
    ))

def check_user_role(user_id):
    try:
        with open(os.path.expanduser("~/.config/.hidden_directory/hidden_users.json"), "r") as file:
            data = json.load(file)

        return data["users"].get(user_id, {}).get("role", "none")
    except (FileNotFoundError, json.JSONDecodeError):
        return "none"

def main():
    console.clear()

    user_id = console.input("\n🔑 [bold cyan]Enter your User ID:[/] ").strip()
    
    role = check_user_role(user_id)
    if role == "none":
        console.print("❌ [bold red]User ID tidak ditemukan![/bold red] Masukkan ID yang valid.")
        return

    console.print("\n[bold green]Login berhasil![/bold green] Welcome to DarkRecon.")
    time.sleep(2)
    
    console.clear()
    banner(role)

    tools_map = {
        "1": whatweb_scan, "2": sqlmap_scan, "3": nuclei_exposed_panel, "4": nmap_scan,
        "5": gobuster_scan, "6": dns_tools, "7": nslookup, "8": subrecon_scan,
        "9": wpscan, "10": dalfox_scan, "11": nuclei_email_extraction, "12": nuclei_technologies,
        "13": nuclei_lfi_scan, "14": nuclei_rce_scan, "15": nuclei_ssrf_scan, "16": "exit"
    }

    while True:
        console.print("[bold yellow]\n📌 Available Tools:[/bold yellow]")
        for num, tool in tools_map.items():
            console.print(f"[bold cyan]{num}[/bold cyan] - {tool.__name__}" if tool != "exit" else "[bold red]16 - Exit[/bold red]")

        choice = console.input("\n⚡ [bold yellow]>> Your choice:[/] ")

        if choice == "16":
            console.print("❌ [bold red]Exiting DarkRecon...[/bold red]")
            break

        if choice in tools_map:
            tool_func = tools_map[choice]
            url = console.input("🌍 [bold cyan]Enter URL or Target:[/] ")
            if callable(tool_func):
                console.print(tool_func(url, user_id) if "user_id" in tool_func.__code__.co_varnames else tool_func(url))
        else:
            console.print("⚠️ [bold yellow]Invalid choice! Try again.[/bold yellow]")
            time.sleep(2)

if __name__ == "__main__":
    main()

