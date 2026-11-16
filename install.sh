#!/bin/bash

echo -e "\e[32m[+] Installing Scythe: Cripper-X Plus...\e[0m"

# 1. Update package lists
echo -e "\e[32m[+] Updating system packages...\e[0m"
sudo apt-get update -y

# 2. Check for Python3
if ! command -v python3 &> /dev/null; then
    echo -e "\e[31m[-] Python3 is not installed. Installing...\e[0m"
    sudo apt-get install -y python3 python3-pip
fi

# 3. Install Hashcat (The core engine)
if ! command -v hashcat &> /dev/null; then
    echo -e "\e[33m[!] Hashcat not found. Installing Hashcat (this may take a minute)...\e[0m"
    sudo apt-get install -y hashcat
else
    echo -e "\e[32m[+] Hashcat is already installed.\e[0m"
fi

# 4. Install Python Dependencies (Handling modern Linux protections)
echo -e "\e[32m[+] Installing Python dependencies (rich, requests, beautifulsoup4)...\e[0m"
# Try normal pip, fallback to --break-system-packages for Kali/Debian
pip3 install requests beautifulsoup4 rich --quiet 2>/dev/null || pip3 install requests beautifulsoup4 rich --break-system-packages --quiet

# 5. Check if scythe.py is in the current folder
if [ ! -f "scythe.py" ]; then
    echo -e "\e[31m[-] ERROR: scythe.py not found in this directory!\e[0m"
    echo -e "\e[33m[!] Make sure install.sh and scythe.py are in the same folder.\e[0m"
    exit 1
fi

# 6. Make Scythe Global
echo -e "\e[32m[+] Installing Scythe to /usr/local/bin/scythe...\e[0m"
sudo cp scythe.py /usr/local/bin/scythe
sudo chmod +x /usr/local/bin/scythe

echo -e "\e[32m[+] Installation complete! Type 'scythe -h' to begin.\e[0m"
