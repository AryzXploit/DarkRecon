import json
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

SECRET_DIR = os.path.expanduser("~/.config/.hidden_directory/")
SECRET_FILE = os.path.join(SECRET_DIR, "hidden_users.json")

os.makedirs(SECRET_DIR, exist_ok=True)

def load_users():
    """Load daftar user dari file JSON."""
    if not os.path.exists(SECRET_FILE):
        return {"users": {}}
    
    with open(SECRET_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    """Simpan daftar user ke file JSON."""
    with open(SECRET_FILE, "w") as file:
        json.dump(users, file, indent=4)

def register_user():
    users = load_users()
    
    console.print(Panel("💀 [bold magenta]DarkRecon User Registration[/bold magenta]", border_style="bright_magenta"))
    
    user_id = console.input("🔑 [bold cyan]Enter your User ID:[/bold cyan] ")
    if user_id in users["users"]:
        console.print(f"❌ [bold red]User ID '{user_id}' already exists![/bold red]")
        return

    console.print("[bold cyan]Choose your access type:[/bold cyan]")
    console.print("1. Free Access")
    console.print("2. Premium Access")

    choice = console.input("\n⚡ [bold yellow]>> Your choice:[/bold yellow] ")

    if choice == "1":
        role = "free"
        console.print("✅ [bold green]You have registered as a Free User.[/bold green]")

    elif choice == "2":
        role = "premium"
        console.print("[bold yellow]Please transfer the payment to the owner at this number:[/bold yellow] [bold green]088224794622[/bold green]")
        console.print("[bold yellow]Once paid, contact the owner to confirm and activate your Premium access.[/bold yellow]")
        
        confirmation = console.input("\n💲 [bold cyan]Have you completed the payment? (yes/no): [/bold cyan]")
        if confirmation.lower() != "yes":
            console.print("❌ [bold red]Payment not completed. Registration cancelled.[/bold red]")
            return

    else:
        console.print("❌ [bold red]Invalid choice![/bold red]")
        return

    users["users"][user_id] = {"role": role}
    save_users(users)
    console.print("✅ [bold green]Registration successful![/bold green]")

if __name__ == "__main__":
    register_user()
