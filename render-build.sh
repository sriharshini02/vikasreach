#!/usr/bin/env bash

# Define installation path
export CHROME_BIN=$HOME/.local/bin/chromium
export CHROMEDRIVER_BIN=$HOME/.local/bin/chromedriver

# Create bin directory if not exists
mkdir -p $HOME/.local/bin

# Install Chromium if not already installed
if [ ! -f "$CHROME_BIN" ]; then
    echo "Installing Chromium..."
    curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
    dpkg -x chrome.deb $HOME/.local
    mv $HOME/.local/opt/google/chrome/chrome $CHROME_BIN
    chmod +x $CHROME_BIN
    rm chrome.deb
else
    echo "Chromium is already installed."
fi

# Install ChromeDriver if not already installed
if [ ! -f "$CHROMEDRIVER_BIN" ]; then
    echo "Installing ChromeDriver..."
    CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    curl -SL "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o chromedriver.zip
    unzip chromedriver.zip -d $HOME/.local/bin
    chmod +x $CHROMEDRIVER_BIN
    rm chromedriver.zip
else
    echo "ChromeDriver is already installed."
fi
