#!/usr/bin/env python3
# Scythe: Cripper-X Plus Engine (Cinematic Decryption v12.2)
# Built by Bliss Chibueze

import argparse
import sys
import os
import subprocess
import tempfile
import time
import random
import shutil
import threading

try:
    from rich.console import Console
    from rich.live import Live
    from rich.text import Text
except ImportError:
    print("[-] Missing dependencies. Please run ./install.sh")
    sys.exit(1)

console = Console(stderr=True) 

# --- MATRIX PROGRESS ANIMATION ---
stop_animation = threading.Event()
progress_state = {"percent": 0}

def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def generate_matrix(active_percent=100):
    cols, lines = get_terminal_size()
    chars = "01ABCDEF!@#$%^&*()_+-=[]{}|;:,.<>?█▓▒░"
    matrix_text = Text()
    active_cols = int((active_percent / 100.0) * cols)
    
    for _ in range(lines):
        for c_idx in range(cols):
            char = random.choice(chars)
            if c_idx < active_cols:
                if random.random() > 0.8:
                    matrix_text.append(char, style="bold green")
                else:
                    matrix_text.append(char, style="dim green")
            else:
                matrix_text.append(char, style="dim red")
        matrix_text.append("\n")
    return matrix_text

def matrix_worker(live, percent=100):
    while not stop_animation.is_set():
        live.update(generate_matrix(percent))
        time.sleep(0.05)

def generate_demon_rules():
    rules = [
        ":", "c", "u", "l", "C", "t", "T", 
        "$1", "$2", "$3", "$4", "$5", "$6", "$7", "$8", "$9", "$0",
        "$1 $2", "$1 $2 $3", "$1 $2 $3 $4", "$1 $2 $3 $4 $5",
        "$2 $0 $2 $0", "$2 $0 $2 $1", "$2 $0 $2 $2", "$2 $0 $2 $3", "$2 $0 $2 $4",
        "$!", "$@", "$#", "$.", "$_", "$!", "$!", "$@", "$@",
        "^!", "^@", "^#", "^1", "^0",
        "sa@", "se3", "si1", "so0", "ss$", "st7", "sb8", "sg9",
        "sa@ $1", "sa@ $!", "se3 $1", "se3 $!", "si1 $1", "so0 $1", "si1 so0",
        "c $1", "c $!", "c $1 $2", "c $1 $2 $3", "c $2 $0 $2 $4", "c $2 $0 $2 $4 $!",
        "d", "f", "sa@ $2 $0 $2 $4 $!", "se3 $2 $0 $2 $4 $!"
    ]
    return "\n".join(rules)

# --- CINEMATIC DECRYPTION ANIMATION ---
def cinematic_decrypt(hash_str, password):
    chars = "!@#$%^&*()_+{}|:<>?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    
    # We don't use screen=True, so it doesn't wipe your terminal
    with Live(console=console, refresh_per_second=30, transient=True) as live:
        # Brief pause to build tension before decryption starts
        text = Text()
        text.append(f"[{hash_str}] -> ", style="cyan")
        text.append("Decrypting...", style="bold yellow")
        live.update(text)
        time.sleep(0.8)
        
        for i in range(len(password) + 1):
            display = []
            for j in range(len(password)):
                if j < i:
                    display.append(password[j])
                else:
                    display.append(random.choice(chars))
            
            text = Text()
            text.append(f"[{hash_str}] -> ", style="cyan")
            
            # If it's the final lock, flash it in green
            if i == len(password):
                text.append("".join(display), style="bold green")
            else:
                text.append("".join(display), style="bold yellow")
                
            live.update(text)
            
            # SLOWER, DRAMATIC SPEED (0.15 seconds per character lock)
            time.sleep(0.15) 
            
    # Print final result permanently so you can copy it
    console.print(f"[{hash_str}] -> [bold green]{password}[/bold green]")

def show_cracked(hashes_file, hash_mode):
    console.print(f"[cyan][*] Querying Hashcat database for {hashes_file}...[/cyan]")
    
    cmd = ["hashcat", "-m", hash_mode, hashes_file, "--show"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip()
        
        if not output:
            console.print("[bold yellow][-] Hashcat says no hashes from this file have been cracked yet.[/bold yellow]")
            return
            
        console.print("[bold green][+] Target acquired. Decrypting...[/bold green]")
        time.sleep(0.5)
        
        for line in output.split('\n'):
            if ':' in line:
                h, p = line.strip().split(':', 1)
                cinematic_decrypt(h, p)
                
    except FileNotFoundError:
        console.print("[bold red][-] Hashcat is not installed![/bold red]")

def main():
    parser = argparse.ArgumentParser(
        description="Scythe: Cripper-X Plus Engine. Built by Bliss Chibueze.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\033[1;36m=== QUICK START GUIDE ===\033[0m

\033[1;33m1. PIPE FROM CRIPPER-X (The Demonic Way):\033[0m
   cripper -C admin,password -l 8 --stdout | scythe --crack hashes.txt

\033[1;33m2. USE YOUR OWN WORDLIST:\033[0m
   scythe -w /usr/share/wordlists/rockyou.txt --crack hashes.txt

\033[1;33m3. VIEW CRACKED PASSWORDS (Cinematic Decryption):\033[0m
   scythe --show hashes.txt

\033[1;31mNOTE:\033[0m Hashcat Mode (-m) defaults to 0 (MD5). 
If you have NTLM hashes, add --hash-mode 1000.
"""
    )
    parser.add_argument("-w", "--wordlist", help="Direct wordlist file (if not piping)")
    parser.add_argument("--crack", help="Target hash file to crack (e.g., hashes.txt)")
    parser.add_argument("--show", help="Show cracked passwords with animation")
    parser.add_argument("--hash-mode", default="0", help="Hashcat mode (default: 0 for MD5)")
    
    args = parser.parse_args()

    if args.show:
        show_cracked(args.show, args.hash_mode)
        return

    is_piping = not sys.stdin.isatty()
    
    if not is_piping and not args.wordlist:
        parser.print_help()
        sys.exit(1)

    temp_wordlist = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt")
    
    final_rules = generate_demon_rules()
    temp_rule = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".rule")
    temp_rule.write(final_rules)
    temp_rule.close()
    rule_file_path = temp_rule.name

    # Start Progress Animation
    progress_state["percent"] = 0
    with Live(generate_matrix(0), refresh_per_second=20, screen=True) as live:
        stop_animation.clear()
        t = threading.Thread(target=matrix_worker, args=(live, progress_state["percent"]), daemon=True)
        t.start()

        count = 0
        if is_piping:
            for line in sys.stdin:
                if line.strip():
                    temp_wordlist.write(line)
                    count += 1
                    if count % 50 == 0 and progress_state["percent"] < 90:
                        progress_state["percent"] += 1
                        stop_animation.set()
                        t.join()
                        stop_animation.clear()
                        t = threading.Thread(target=matrix_worker, args=(live, progress_state["percent"]), daemon=True)
                        t.start()
        elif args.wordlist:
            try:
                with open(args.wordlist, 'r') as f:
                    for line in f:
                        if line.strip():
                            temp_wordlist.write(line)
                            count += 1
                            if count % 500 == 0 and progress_state["percent"] < 90:
                                progress_state["percent"] += 1
                                stop_animation.set()
                                t.join()
                                stop_animation.clear()
                                t = threading.Thread(target=matrix_worker, args=(live, progress_state["percent"]), daemon=True)
                                t.start()
            except FileNotFoundError:
                stop_animation.set()
                console.print(f"[bold red][-] File not found: {args.wordlist}[/bold red]")
                sys.exit(1)
                
        temp_wordlist.close()
        
        progress_state["percent"] = 100
        stop_animation.set()
        t.join()
        
        stop_animation.clear()
        t = threading.Thread(target=matrix_worker, args=(live, 100), daemon=True)
        t.start()
        time.sleep(0.5)
        stop_animation.set()
        t.join()

    if count == 0:
        console.print("[bold red][-] Error: 0 words received![/bold red]")
        os.remove(temp_wordlist.name)
        os.remove(rule_file_path)
        sys.exit(1)

    if args.crack:
        console.print("\n" + "="*60)
        console.print("[bold red]>>> SYSTEM BREACH COMPLETE. LAUNCHING GPU <<<[/bold red]")
        console.print(f"[cyan][*] Target: {args.crack}[/cyan]")
        console.print(f"[cyan][*] Base Words: {count}[/cyan]")
        console.print(f"[cyan][*] Rules Applied: 65 Demonic Mutations[/cyan]")
        console.print(f"[cyan][*] Run 'scythe --show {args.crack}' to see decrypted passwords.[/cyan]")
        console.print("="*60 + "\n")
        
        hashcat_cmd = [
            "hashcat", "-m", args.hash_mode, "-a", "0", 
            args.crack, temp_wordlist.name, 
            "-r", rule_file_path, 
            "--status", "--status-timer", "2"
        ]
        
        try:
            subprocess.run(hashcat_cmd)
        except FileNotFoundError:
            console.print("[bold red][-] Hashcat is not installed![/bold red]")
        finally:
            if os.path.exists(rule_file_path): os.remove(rule_file_path)
            if os.path.exists(temp_wordlist.name): os.remove(temp_wordlist.name)

if __name__ == "__main__":
    main()
