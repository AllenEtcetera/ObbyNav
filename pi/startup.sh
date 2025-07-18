#!/bin/bash

cd /home/user

# Remove the old folder if it exists
rm -rf ObbyNav

# Clone the latest version
git clone https://github.com/AllenEtcetera/ObbyNav.git

# Run the desired script (adjust the filename below)
chmod +rx /home/user/ObbyNav/navbrain.py
/home/user/ObbyNav/navbrain.py
