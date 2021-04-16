#!/usr/bin/env bash

# After the previous procedure we go on sqlite3 tool for table part
sqlite3 watchDogDB.sqlite <<'END_SQL'
# read .sql command to create the table. Table for movies project
.read sqlCommands/createMoviesTb.sql
END_SQL
#Here ends the command for sqlite3
