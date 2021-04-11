#!/usr/bin/env bash

#The program runs with the bellow command
#./shellScriptWithInput -u scott -p s3cr3t (-a|-ab|-b)

while getopts :u:p:ab options
do
	case $options in
		u) user=$OPTARG;;
		p) pass=$OPTARG;;
		a) echo "User add A flag";;
		b) echo "User add B flag";;
		?) echo "User add unknown flag: $OPTARG !"
	esac
done

echo "user: $user / pass: $pass"
