#!/usr/bin/bash

me=$(whoami)
cd /home/$me/clickoor-v2

echo "Installing dependencies"
sudo apt install python3-pyqt5.qtmultimedia
sudo apt-get install python3-pyqt5.qtsvg
sudo apt-get install libqt5multimedia5-plugins
pip3 install pyqtdarktheme --break-system-packages
pip3 install arweave-python-client --break-system-packages

# replace pi with $me in camera.desktop file
sed -i "s/pi/$me/" camera-v2.desktop

sudo cp camera-v2.desktop /usr/share/applications


chmod +x ./start.sh
echo "Setup Done! Checkout Menu > Other > Clickoor Camera V2"
