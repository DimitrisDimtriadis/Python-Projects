#!/usr/bin/env bash

#To update the existand os
sudo apt update
sudo apt upgrade

# First argument used for installation and the second one to check the version
installSpecificTool(){
    #Need to check if demanded tool is installed
    $2 --version > /dev/null 2>&1 &
    #If previously command was success (already exists) the var takes value 1
    isToolInstalled=$?
    if [ $isToolInstalled != '0' ]
    then
        # Excecute bash script to install the sqlite3
        sudo apt install $1
        $2 --version        
    else
        echo "$1 is already installed !"
    fi    
}

echo "Checking about SQLite..."
installSpecificTool sqlite3 sqlite3

echo "Checking about Python..."
installSpecificTool python3.8 python3

echo "Checking about pip..."
installSpecificTool python3-pip pip3

parentFilePath=$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# Initialize the DataBase with MoviesTb (table)
cd $parentFilePath; chmod 755 shellScriptAggregator.sh
cd DBUtil; chmod 755 storageConfigure.sh; sh ./storageConfigure.sh