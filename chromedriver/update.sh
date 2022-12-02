#!/usr/bin/bash
version=$(chromium-browser --version | cut -d ' ' -f2 | xargs)
# debug
# version='108.0.5359.71' 
existing_version=$(cat linux-version | xargs)

driver_version=$(./chromedriver --version)
echo Driver version $driver_version

echo Driver: $existing_version
echo Chrome: $version

if [[ $version == $existing_version ]]; then
    echo No update needed.
else
    url="https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip"
    echo Download new driver $url
    curl -o chromedriver.zip $url 
    unzip -o chromedriver.zip
    if [[ $? -eq 0 ]]; then 
        echo Driver updated to $version
        echo $version > linux-version
        rm -rf *zip*
    else
        echo There was something wrong when updating. Exit.
    fi
    
fi
