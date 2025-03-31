#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver in a writable directory..."

# Create a local bin folder (Render has a read-only system, so we install locally)
mkdir -p $HOME/chrome
mkdir -p $HOME/chromedriver

# Install Chrome (Download a portable version)
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > $HOME/chrome/google-chrome.deb
dpkg -x $HOME/chrome/google-chrome.deb $HOME/chrome/

# Set Chrome binary path
export CHROME_BIN=$HOME/chrome/opt/google/chrome/google-chrome

# Find the correct Chrome version
CHROME_VERSION=$($CHROME_BIN --version | awk '{print $3}' | cut -d '.' -f 1)

# Download ChromeDriver that matches Chrome version
wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip" -O $HOME/chromedriver/chromedriver.zip
unzip $HOME/chromedriver/chromedriver.zip -d $HOME/chromedriver/
chmod +x $HOME/chromedriver/chromedriver

echo "Chrome and ChromeDriver installed successfully in $HOME!"

