#!/bin/bash

sudo apt update

sudo apt install golang -y

sudo apt install -y pipx

sudo apt install -y docker.io
sudo systemctl enable docker --now

# go tools
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
pipx install arjun
sudo apt install -y subfinder
sudo apt install -y nuclei
sudo apt install -y eyewitness
pipx install uro
go install github.com/tomnomnom/gf@latest
go install github.com/tomnomnom/qsreplace@latest
go install github.com/tomnomnom/qsreplace@latest

# gf setup
mkdir -p ~/.gf
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp Gf-Patterns/*.json ~/.gf
sudo mv go/bin/* /usr/bin/

echo -e "\e[1;32mDONE!\e[0m"
