#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver..."

export INSTALL_DIR="/opt/render"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"
export CHROME_DIR="$INSTALL_DIR/chrome"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

CHROME_VERSION="134.0.6998.165"

# Install Chrome
wget -qO- "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O $CHROME_DIR/chrome.zip
unzip -o $CHROME_DIR/chrome.zip -d $CHROME_DIR/
export CHROME_BIN="$CHROME_DIR/chrome-linux64/chrome"

# Install ChromeDriver
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip
unzip -o $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/
mv $CHROMEDRIVER_DIR/chromedriver-linux64/chromedriver $CHROMEDRIVER_DIR/

chmod +x $CHROMEDRIVER_DIR/chromedriver

# Print installed paths
echo "🔍 Checking Installed Paths..."
echo "Chrome Path: $(command -v $CHROME_BIN || echo 'Not found')"
echo "ChromeDriver Path: $(command -v $CHROMEDRIVER_DIR/chromedriver || echo 'Not found')"

ls -lah $CHROME_BIN
ls -lah $CHROMEDRIVER_DIR/chromedriver

# Ensure permissions
chmod +x $CHROME_BIN
chmod +x $CHROMEDRIVER_DIR/chromedriver

echo "✅ Chrome and ChromeDriver installed successfully!"
