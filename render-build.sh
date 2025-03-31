#!/usr/bin/env bash

echo "🚀 Installing Chrome & ChromeDriver..."

# Define installation directories
export INSTALL_DIR="/opt/render"
export CHROMEDRIVER_DIR="$INSTALL_DIR/chromedriver"
export CHROME_DIR="$INSTALL_DIR/chrome"

mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Define latest Chrome version
CHROME_VERSION="134.0.6998.165"

# Install Chrome
echo "📥 Downloading Chrome..."
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O $CHROME_DIR/chrome.zip
unzip -o $CHROME_DIR/chrome.zip -d $CHROME_DIR/
export CHROME_BIN="$CHROME_DIR/chrome-linux64/chrome"

# Install ChromeDriver
echo "📥 Downloading ChromeDriver..."
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" -O $CHROMEDRIVER_DIR/chromedriver.zip
unzip -o $CHROMEDRIVER_DIR/chromedriver.zip -d $CHROMEDRIVER_DIR/

# Move ChromeDriver binary
mv $CHROMEDRIVER_DIR/chromedriver-linux64/chromedriver $CHROMEDRIVER_DIR/
export CHROMEDRIVER_BIN="$CHROMEDRIVER_DIR/chromedriver"

# Set execution permissions
chmod +x $CHROME_BIN
chmod +x $CHROMEDRIVER_BIN

# Debugging: Print paths
echo "🔍 Installed Paths:"
echo "  - Chrome: $CHROME_BIN"
echo "  - ChromeDriver: $CHROMEDRIVER_BIN"

# Verify installation
if [ -f "$CHROME_BIN" ]; then
    echo "✅ Chrome installed successfully!"
else
    echo "❌ Chrome installation failed!"
    exit 1
fi

if [ -f "$CHROMEDRIVER_BIN" ]; then
    echo "✅ ChromeDriver installed successfully!"
else
    echo "❌ ChromeDriver installation failed!"
    exit 1
fi

# Debugging: Check if commands are accessible
echo "🔍 Checking command availability..."
echo "Chrome Path: $(command -v $CHROME_BIN || echo 'Not found')"
echo "ChromeDriver Path: $(command -v $CHROMEDRIVER_BIN || echo 'Not found')"

# Debugging: List contents
ls -lah $CHROME_BIN
ls -lah $CHROMEDRIVER_BIN

# Export paths for Selenium
export PATH="$CHROMEDRIVER_DIR:$PATH"

echo "🚀 Chrome & ChromeDriver Setup Complete!"
