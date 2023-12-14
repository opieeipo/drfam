#!/bin/bash
#python Windows setup
#virtual setup
mkdir .dev.wsl.env
mkdir .pilot.wsl.env
#build the environments
python3 -m venv .dev.wsl.env
source ./.dev.wsl.env/bin/activate
pip cache purge
pip install -r wsl.requirements.txt
deactivate
python3 -m venv .pilot.wsl.env
source ./.pilot.wsl.env/bin/activate
pip install -r wsl.requirements.txt
deactivate
