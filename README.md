# 🐀 Scythe: Cripper-X Plus Engine

![Version](https://img.shields.io/badge/Version-12.2-brightgreen)
![Author](https://img.shields.io/badge/Author-Bliss%20Chibueze-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali%20%7C%20Debian-lightgrey)

**Scythe** is an advanced, GPU-accelerated password cracking orchestrator designed to be the ultimate companion to `Cripper-X`. Built by **Bliss Chibueze**, Scythe bridges the gap between raw wordlist generation and Hashcat's immense processing power.

Instead of downloading massive 10GB wordlists, Scythe allows you to dynamically generate highly targeted passwords, inject demonic Hashcat rules on the fly, and watch the cracking process through a cinematic, Hollywood-style terminal interface.

---

## ⚡ Features

*   **The Demonic Pipeline:** Pipe `Cripper-X` directly into Scythe. Scythe analyzes the stream and automatically applies 65+ aggressive Hashcat mutation rules (Leetspeak, Year appending, Capitalization).
*   **Zero-Bloat Rules:** No need to download external `.rule` files. Scythe dynamically generates its own rules based on the target context.
*   **Cinematic Matrix Rain:** A full-terminal, progress-based Matrix animation that fills up as it receives data from Cripper-X.
*   **Hollywood Decryption (`--show`):** Watch passwords unscramble character-by-character with dramatic tension when you view your cracked hashes.
*   **Auto-Installer:** A built-in installer that automatically configures Python dependencies and global execution paths.

---

## 🛠️ Installation

Scythe is designed for Linux environments (Kali, Debian, Ubuntu) and requires `hashcat` to be installed.

1. Clone the repository:
    git clone https://github.com/YOUR_USERNAME/Scythe.git
    cd Scythe

2. Run the automatic installer:
    chmod +x install.sh
    ./install.sh

*This will install `requests`, `beautifulsoup4`, and `rich`, and move Scythe to your `/usr/local/bin` directory.*

---

## 🚀 Usage (Quick Start)

Once installed, you can call `scythe` from anywhere in your terminal.

### 1. The Demonic Pipeline (Generate & Crack)
Pipe Cripper-X directly into Scythe. It will catch the words, generate demonic rules, and fire into the GPU.
    cripper -C admin,password -l 8 --stdout | scythe --crack hashes.txt --hash-mode 0

*(Note: `--hash-mode 0` is for MD5. Use `1000` for NTLM.)*

### 2. Using a Pre-existing Wordlist
Already have a wordlist? Feed it directly to Scythe.
    scythe -w /usr/share/wordlists/rockyou.txt --crack hashes.txt

### 3. The Hollywood Decryption (`--show`)
Once Hashcat finishes, view the cracked passwords with the cinematic unscrambling animation.
    scythe --show hashes.txt

### 4. Help Menu
For a dumb-ass proof guide on how to use the tool:
    scythe -h

---

## 👨‍💻 Author

**Bliss Chibueze**
*Built for the ones who want to see the matrix.*

---

## ⚠️ Disclaimer
This tool is intended for educational purposes and authorized penetration testing only. Do not use Scythe on systems you do not own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.
