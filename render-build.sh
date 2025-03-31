#!/usr/bin/env bash

echo "Installing Chrome & ChromeDriver..."

export INSTALL_DIR="/opt/render"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"
export CHROME_DIR="$INSTALL_DIR/chrome"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Define latest Chrome version
CHROME_VERSION="134.0.6998.165"

# Install Chrome
wget -qO- "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O $CHROME_DIR/chrome.zip
unzip -o $CHROME_DIR/chrome.zip -d $CHROME_DIR/
export CHROME_BIN="$CHROME_DIR/chrome-linux64/chrome"

# Verify Chrome installation
if [ ! -f "$CHROME_BIN" ]; then
    echo "❌ Chrome installation failed!"
    exit 1
fi

# Install ChromeDriver
wget "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip
unzip -o $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/

# Move ChromeDriver binary to expected location
mv $CHROMEDRIVER_DIR/chromedriver-linux64/chromedriver $CHROMEDRIVER_DIR/
chmod +x $CHROMEDRIVER_DIR/chromedriver

# Verify ChromeDriver installation
if [ ! -f "$CHROMEDRIVER_DIR/chromedriver" ]; then
    echo "❌ ChromeDriver installation failed!"
    exit 1
fi

# Print installed paths
echo "✅ Chrome and ChromeDriver installed successfully!"

# Debugging: Show directory structure
echo "📂 Listing contents of /opt/render:"
ls -l /opt/render

echo "📂 Listing contents of $CHROME_DIR:"
ls -l $CHROME_DIR

echo "📂 Listing contents of $CHROMEDRIVER_DIR:"
ls -l $CHROMEDRIVER_DIR

# Print absolute paths
echo "🔍 Expected Chrome Path: $CHROME_BIN"
echo "🔍 Expected ChromeDriver Path: $CHROMEDRIVER_DIR/chromedriver"

# Double-check Chrome and ChromeDriver locations
echo "🔍 Checking Chrome binary existence..."
if [ -x "$CHROME_BIN" ]; then
    echo "✅ Chrome found at: $CHROME_BIN"
else
    echo "❌ Chrome not found at expected location!"
fi

echo "🔍 Checking ChromeDriver binary existence..."
if [ -x "$CHROMEDRIVER_DIR/chromedriver" ]; then
    echo "✅ ChromeDriver found at: $CHROMEDRIVER_DIR/chromedriver"
else
    echo "❌ ChromeDriver not found at expected location!"
fi
