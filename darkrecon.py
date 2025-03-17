import os
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

def check_user_role(user_id):
    file_path = os.path.expanduser("~/.config/.hidden_directory/hidden_users.json")
    if not os.path.exists(file_path):
        return "none"

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data["users"].get(user_id, {}).get("role", "none")
    except (json.JSONDecodeError, KeyError):
        return "none"

def run_scan(scan_func, user_id, *args):
    try:
        console.print("\n⚡ Running scan...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Scanning..."),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Scanning...", total=100)
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.05)  # Dipercepat loading-nya

        console.print(f"\n🚀 Executing: {scan_func.__name__} with args: {args}\n")
        
        result = scan_func(*args, user_id) if scan_func in premium_tools else scan_func(*args)

        if not result.strip():
            console.print("\n⚠️ [bold yellow]No vulnerabilities found or no response received.[/bold yellow]")
        else:
            console.print(f"\n{result.strip()}")

    except Exception as e:
        console.print(f"\n❌ [bold red]Error:[/] {e}")

    console.input("\n🔄 [bold white]Press Enter to continue...[/bold white]")

def main():
    console.clear()

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

    console.print("\n[bold green]Login berhasil![/bold green] Welcome to DarkRecon.")
    time.sleep(1)

    while True:
        console.clear()
        menu()
        choice = console.input("\n⚡ [bold yellow]>> Your choice:[/] ")

        if choice == "13":
            console.print("\n❌ [bold red]Exiting DarkRecon...[/bold red]\n")
            time.sleep(1)
            break

        if choice in tools_map:
            tool_func = tools_map[choice]
            if tool_func == "exit":
                break

            if tool_func in premium_tools and role not in ["premium", "admin"]:
                console.print("🔒 [bold red]Access Denied! Upgrade to premium.[/bold red]")
            else:
                target = console.input("\n🌍 [bold cyan]Enter Target (URL/IP):[/] ").strip()
                run_scan(tool_func, user_id, target)

        else:
            console.print("⚠️ [bold yellow]Invalid choice! Try again.[/bold yellow]")
