from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from tools import *
import os
import time
import json  # Jangan lupa import json!

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

        if user_id in data["users"]:
            return data["users"][user_id]["role"]
        else:
            return "none"
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
                time.sleep(0.11)
        
        time.sleep(2)
        
        console.print(f"\n⚡ Running: {scan_func.__name__} with args: {args}\n")
        
        if scan_func in [subrecon_scan, wpscan, dalfox_scan, nuclei_email_extraction, nuclei_technologies]:
            result = scan_func(*args, user_id)
        else:
            result = scan_func(*args)
        
        if not result or result.strip() == "":
            console.print("\n⚠️ [bold yellow]No vulnerabilities found or no response received.[/bold yellow]")
        else:
            console.print(f"\n{result.strip()}")

    except Exception as e:
        console.print(f"\n❌ [bold red]Error:[/] {e}")

    console.input("\n🔄 [bold white]Press Enter to continue...[/bold white]")

def main():
    console.clear()
    
    banner("none")

    if not os.path.exists(os.path.expanduser("~/.config/.hidden_directory/hidden_users.json")):
        os.makedirs(os.path.expanduser("~/.config/.hidden_directory/"), exist_ok=True)
        with open(os.path.expanduser("~/.config/.hidden_directory/hidden_users.json"), "w") as file:
            file.write('{"users": {}}')

    while True:
        user_id = console.input("\n🔑 [bold cyan]Enter your User ID:[/] ").strip()
        
        if not user_id:
            console.print("⚠️ [bold yellow]User ID tidak boleh kosong![/bold yellow]")
            continue

        role = check_user_role(user_id)
        
        if role == "none":
            console.print("❌ [bold red]User ID tidak ditemukan![/bold red] Masukkan ID yang valid.")
            continue

        break

    console.clear()
    banner(role)

    tools_map = {
        "1": (whatweb_scan, "🌍 [bold cyan]Enter URL: [/bold cyan]"),
        "2": (sqlmap_scan, "🛡️ [bold cyan]Enter URL: [/bold cyan]"),
        "3": (nuclei_exposed_panel, "🔎 [bold cyan]Enter URL: [/bold cyan]"),
        "4": (nmap_scan, "📡 [bold cyan]Enter Target (IP/Domain): [/bold cyan]"),
        "5": (gobuster_scan, "🚀 [bold cyan]Enter URL: [/bold cyan]", "📜 [bold cyan]Enter Wordlist Path: [/bold cyan]"),
        "6": (dns_tools, "🌐 [bold cyan]Enter Domain: [/bold cyan]"),
        "7": (nslookup, "🔍 [bold cyan]Enter Domain: [/bold cyan]"),
        "8": (subrecon_scan, "🔬 [bold cyan]Enter Domain: [/bold cyan]"),
        "9": (wpscan, "📝 [bold cyan]Enter URL: [/bold cyan]"),
        "10": (dalfox_scan, "🎯 [bold cyan]Enter URL: [/bold cyan]"),
        "11": (nuclei_email_extraction, "📧 [bold cyan]Enter URL: [/bold cyan]"),
        "12": (nuclei_technologies, "🖥️ [bold cyan]Enter URL: [/bold cyan]"),
        "13": "exit"
    }

    while True:
        console.clear()
        banner(role)
        menu()

        choice = console.input("\n⚡ [bold yellow]>> Your choice:[/] ")

        if choice == "13":
            console.print("❌ [bold red]Exiting DarkRecon...[/bold red]")
            break

        if choice in tools_map:
            if choice == "5":
                tool_func, prompt_url, prompt_wordlist = tools_map[choice]
                url = console.input(prompt_url)
                wordlist = console.input(prompt_wordlist)
                run_scan(tool_func, user_id, url, wordlist)
            else:
                tool_func, prompt = tools_map[choice]
                url = console.input(prompt)
                run_scan(tool_func, user_id, url)
        else:
            console.print("⚠️ [bold yellow]Invalid choice! Try again.[/bold yellow]")

if __name__ == "__main__":
    main()
