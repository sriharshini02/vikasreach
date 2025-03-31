#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver in a writable directory..."

# Define directories
export INSTALL_DIR="$HOME/render"
export CHROME_DIR="$INSTALL_DIR/chrome"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Install Chrome (Portable version)
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > $CHROME_DIR/google-chrome.deb
dpkg -x $CHROME_DIR/google-chrome.deb $CHROME_DIR/

# Set Chrome binary path
export CHROME_BIN=$CHROME_DIR/opt/google/chrome/google-chrome

# Check installed Chrome version
CHROME_VERSION=$($CHROME_BIN --version | awk '{print $3}' | cut -d '.' -f 1)

# Check the latest compatible ChromeDriver version
LATEST_DRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}"
CHROMEDRIVER_VERSION=$(wget -qO- $LATEST_DRIVER_URL)

# Download and install ChromeDriver
wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip
unzip $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/
chmod +x $CHROMEDRIVER_DIR/chromedriver

echo "Chrome and ChromeDriver installed successfully!"
