# 🎯 MySQL Hunter

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<p align="center">
  <strong>Fast, multi-threaded MySQL brute-force tool with live progress tracking.</strong>
  <br>
  <em>For educational and authorized penetration testing only.</em>
</p>

---

## ✨ Features

- 🚀 Multi-threaded attacks with adjustable thread count
- 🎨 Beautiful CLI with color-coded output & ASCII banner
- 📊 Live progress bar with speed, ETA & statistics
- 🔄 Interactive mode + command-line mode
- 💾 Auto-saves found credentials

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/mysql-hunter.git
cd mysql-hunter
pip install mysql-connector-python
```

---

## 🚀 Usage

### Interactive Mode
```bash
python mysql_hunter.py
```

### Command-Line Mode
```bash
python mysql_hunter.py -H <host> -u <username> -w <wordlist>

# Example
python mysql_hunter.py -H 192.168.1.100 -u root -w rockyou.txt -t 20
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-H` | Target host IP | Required |
| `-P` | MySQL port | 3306 |
| `-u` | Username | Required |
| `-w` | Wordlist path | Required |
| `-t` | Threads | 10 |
| `-d` | Database name | None |
| `-v` | Verbose mode | False |

---

## 🧪 Quick Test Lab

```bash
# Start MySQL container
docker run -d --name mysql-lab -e MYSQL_ROOT_PASSWORD=password123 -p 3306:3306 mysql:8.0

# Run the hunt
python mysql_hunter.py -H 127.0.0.1 -u root -w wordlist.txt
```

---

## 📸 Preview

```
  🔥 HUNT STARTED 🔥

  [██████████████▓░░░░░░░░░░░░░░░] 45.2% 4,521/10,001 ⚡ 245.3/s ⏱ ETA: 22s → password123

  ╔════════════════════════════════════════════════════════╗
  ║            🎯 TARGET CAPTURED! 🎯                      ║
  ╚════════════════════════════════════════════════════════╝

  Host:     192.168.1.100:3306
  Username: root
  Password: secretpass123
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing only**. Unauthorized access to computer systems is illegal. Use responsibly.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>⭐ Star this repo if you find it useful!</strong>
  <br>
  <strong>🎯 Happy Hunting!</strong>
</p>
