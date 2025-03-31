#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver..."

export INSTALL_DIR="/opt/render"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"
export CHROME_DIR="$INSTALL_DIR/chrome"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Install Chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > $CHROME_DIR/google-chrome.deb
dpkg -x $CHROME_DIR/google-chrome.deb $CHROME_DIR/
export CHROME_BIN=$CHROME_DIR/opt/google/chrome/google-chrome

# Verify Chrome installation
if [ ! -f "$CHROME_BIN" ]; then
    echo "❌ Chrome installation failed!"
    exit 1
fi

# Get Chrome version
CHROME_VERSION=$($CHROME_BIN --version | awk '{print $3}' | cut -d '.' -f 1)

# Fetch latest matching ChromeDriver version
LATEST_DRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}"
CHROMEDRIVER_VERSION=$(wget -qO- $LATEST_DRIVER_URL)

# Remove old files
rm -f $CHROMEDRIVER_DIR/chromedriver.zip
rm -f $CHROMEDRIVER_DIR/chromedriver

# Download new ChromeDriver
wget "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip

# Verify download
if [ ! -f "$CHROMEDRIVER_DIR/chromedriver.zip" ]; then
    echo "❌ ChromeDriver download failed!"
    exit 1
fi

# Extract and set permissions
unzip -o $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/
chmod +x $CHROMEDRIVER_DIR/chromedriver

# Final verification
if [ ! -f "$CHROMEDRIVER_DIR/chromedriver" ]; then
    echo "❌ ChromeDriver installation failed!"
    exit 1
fi

echo "✅ Chrome and ChromeDriver installed successfully at $CHROMEDRIVER_DIR!"
