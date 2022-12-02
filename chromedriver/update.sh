#!/usr/bin/bash
chrome_version=$(chromium-browser --version | cut -d ' ' -f2 | xargs)
driver_version=$(./chromedriver --version | cut -d ' ' -f2 | xargs)

echo Driver: $driver_version
echo Chrome: $chrome_version

if [[ $chrome_version == $driver_version ]]; then
    echo No update needed.
else
    url="https://chromedriver.storage.googleapis.com/$chrome_version/chromedriver_linux64.zip"
    echo Download new driver $url
    curl -o chromedriver.zip $url 
    unzip -o chromedriver.zip
    if [[ $? -eq 0 ]]; then
        echo Driver updated to $chrome_version
        chmod +x chromedriver
        ./chromedriver --version
        rm -rf *zip*
    else
        echo There was something wrong when updating. Exit.
    fi
    
fi
