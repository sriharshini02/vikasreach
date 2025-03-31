#!/usr/bin/env bash

# Install Chromium
if ! command -v chromium &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "Installing Chromium..."
    sudo apt-get update
    sudo apt-get install -y chromium-browser
else
    echo "Chromium is already installed."
fi
