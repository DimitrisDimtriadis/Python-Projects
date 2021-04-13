#!/usr/bin/env bash

#Need to check if sqlite3 is installed
which sqlite3 > /dev/null 2>&1 &
#If previously command was success (sqlite3 exists) the var takes value 1
isSqliteInstalled=$?

if [ $isSqliteInstalled != '0' ]
then
	# Excecute bash script to install the sqlite3
	./sqlite3Install.sh
fi

# After the previous procedure we go on sqlite3 tool for table part
sqlite3 watchDogDB.sqlite <<'END_SQL'
# read .sql command to create the table
.read sqlCommands/createMoviesTb.sql #Table for movies project
END_SQL #Here ends the command for sqlite3

echo "Script finished"
