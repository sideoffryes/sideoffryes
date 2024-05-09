# fetch and install all updates
echo "[*] sudo apt update && sudo apt upgrade"
sudo apt update && sudo apt upgrade

# python, pip, pwntools, and ROPgadget
echo "[*] apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential"
sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
echo "[*] python3 -m pip install --upgrade pip"
python3 -m pip install --upgrade pip
echo "[*] python3 -m pip install --upgrade pwntools"
python3 -m pip install --upgrade pwntools
echo "[*] sudo -H python3 -m pip install ROPgadget"
sudo -H python3 -m pip install ROPgadget

# gdb
echo "[*] sudo apt install gdb"
sudo apt install gdb

# gef
echo "[*] bash -c '$(wget --no-check-certificate https://gef.blah.cat/sh -O -)'"
bash -c "$(wget --no-check-certificate https://gef.blah.cat/sh -O -)"

# eog
echo "[*] sudo apt install eog"
sudo apt install eog

# net-tools
echo "[*] sudo apt install net-tools"
sudo apt install net-tools

# unzip
echo "[*] sudo apt install unzip && sudo apt install zip"
sudo apt install unzip && sudo apt install zip