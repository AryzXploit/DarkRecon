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
        f"🆙 [bold white]Version:[/] 1.2\n"  
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

def menu():
    table = Table(title="🛠️ [bold cyan]Available Tools[/bold cyan]", show_header=True, header_style="bold white", border_style="bright_blue")
    table.add_column("No", style="bold yellow", width=5)
    table.add_column("Tool", style="bold cyan")

    tools = [
        "🌍 WhatWeb", "🛡️ SQLMap", "🔎 Nuclei (Exposed Panel)", "📡 Nmap", "🚀 GoBuster",
        "🌐 DNS Tools", "🔍 Nslookup",
        "[PREMIUM] 🔬 SubRecon & Amass", "[PREMIUM] 📝 WPScan", "[PREMIUM] 🎯 Dalfox",
        "[PREMIUM] 📧 Nuclei (Email Extraction)", "[PREMIUM] 🖥️ Nuclei (Technologies Detection)",
        "[PREMIUM] 🛠️ Nuclei (LFI Scan)", "[PREMIUM] 🔥 Nuclei (RCE Scan)", "[PREMIUM] 🌍 Nuclei (SSRF Scan)",
        "[bold red]❌ Exit Framework[/bold red]"
    ]

    for i, tool in enumerate(tools, 1):
        table.add_row(str(i), tool)

    console.print(table)

def run_scan(scan_func, user_id, *args):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Scanning..."),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Scanning...", total=100)
            
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.1)
        
        console.print(f"\n⚡ Running: {scan_func.__name__} with args: {args}\n")
        
        result = scan_func(*args, user_id) if "user_id" in scan_func.__code__.co_varnames else scan_func(*args)
        
        if not result or result.strip() == "":
            console.print("\n⚠️ [bold yellow]No vulnerabilities found or no response received.[/bold yellow]")
        else:
            console.print(f"\n{result.strip()}")

    except Exception as e:
        console.print(f"\n❌ [bold red]Error:[/] {e}")

    console.input("\n🔄 [bold white]Press Enter to continue...[/bold white]")

def main():
    console.clear()

    user_id = console.input("\n🔑 [bold cyan]Enter your User ID:[/] ").strip()
    
    role = check_user_role(user_id)
    if role == "none":
        console.print("❌ [bold red]User ID tidak ditemukan![/bold red] Masukkan ID yang valid.")
        return

    # Ubah sambutan berdasarkan role
    role_text = "Premium Member" if role == "premium" else "Free Member"
    console.print(f"\n✅ [bold green]Login berhasil![/bold green] Welcome, [bold cyan]{role_text}[/bold cyan] to DarkRecon.")
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
        console.clear()
        banner(role)
        menu()

        choice = console.input("\n⚡ [bold yellow]>> Your choice:[/] ")

        if choice == "16":
            console.print("❌ [bold red]Exiting DarkRecon...[/bold red]")
            break

        if choice in tools_map:
            tool_func = tools_map[choice]
            url = console.input("🌍 [bold cyan]Enter URL or Target:[/] ")
            run_scan(tool_func, user_id, url)
        else:
            console.print("⚠️ [bold yellow]Invalid choice! Try again.[/bold yellow]")
            time.sleep(2)

if __name__ == "__main__":
    main()
