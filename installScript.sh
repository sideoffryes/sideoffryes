# fetch and install all updates
echo "[*] sudo apt update && sudo apt upgrade -y"
sudo apt update && sudo apt upgrade -y

# python, pip, pwntools, and ROPgadget
echo "[*] sudo apt install -y python3 python3-pip git build-essential"
sudo sudo apt install -y python3 python3-pip git build-essential

# gdb
echo "[*] sudo apt install gdb"
sudo apt install gdb

# gef
echo "[*] bash -c '$(wget --no-check-certificate https://gef.blah.cat/sh -O -)'"
bash -c "$(wget --no-check-certificate https://gef.blah.cat/sh -O -)"

# net-tools
echo "[*] sudo apt install net-tools"
sudo apt install net-tools

# unzip
echo "[*] sudo apt install unzip && sudo apt install zip"
sudo apt install unzip && sudo apt install zip

# htop 
echo "[*] sudo apt install htop"
sudo apt install htop

# miniconda
echo "mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all"
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all