#!/bin/bash
# Install Chrome and ChromeDriver
echo "Installing Chrome and ChromeDriver..."
sudo apt-get update
sudo apt-get install -y chromium-browser
sudo apt-get install -y chromium-chromedriver
echo "Chrome and ChromeDriver installation complete."
