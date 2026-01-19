#!/bin/bash

set -e
echo "installing ypf"

#arch
echo "installing packages"
sudo pacman -S --needed --noconfirm python-pandas python-numpy python-matplotlib python-yaml python-requests

echo "configuring venv!"
python -m venv venv --system-site-packages
source venv/bin/activate

echo "installing other requirements!"
pip install rich networkx flask packaging matplotlib

echo "Completed!!!"
