#!/usr/bin/env bash

source ./Scripts/activate

if ! command -v pyinstaller &> /dev/null; then
  echo "PyInstaller is not installed. Please install it."
  sleep 8
  exit 1
fi

read -p "Confirm to build .exe file - Y / N: " name
if [ "${name,,}" == "y"  ]; then
  echo "File is building..."
  pyinstaller --onefile --name xGNHL --icon=Img/nhl.ico main.py
  if [ $? -ne 0 ]; then
    echo "Error building file."
  else
    echo "File built successfully!"
  fi
else
  echo "File building cancelled."
fi

sleep 8
exit 0