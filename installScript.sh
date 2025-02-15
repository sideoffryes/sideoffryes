# fetch and install all updates
sudo apt update && sudo apt upgrade -y

sudo sudo apt install -y python3 python3-pip git build-essential gdb net-tools unzip zip htop

# gef
echo "[*] bash -c '$(wget --no-check-certificate https://gef.blah.cat/sh -O -)'"
bash -c "$(wget --no-check-certificate https://gef.blah.cat/sh -O -)"

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