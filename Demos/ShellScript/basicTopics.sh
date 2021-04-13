#!/usr/bin/env bash

#Check the Bash Version before do anything else. If it is below than 4 then exit from script
[[ ! $BASH_VERSINFO -ge 4 ]] && echo "---Check Bash Version" && echo "You 'll need to update to Bash 4+" && exit

echo
#Colorize text
echo -n "---"
echo "Colorize text"
ulinered="\033[4;31;40m"
red="\033[31;40m"
none="\033[0m"
echo -e $ulinered"ERROR:"$none$red" Something went wrong."$none

declare -i a=3
b=43
b=4

echo
# IF statements
echo "---IF statements"
if [[ $a -gt 4 ]]; then
	echo "$a is greater than 4."
else 
	echo "$a is not greater than 4."
fi
if (( $a > 4)); then echo "$a is greater than 4."; else echo "$a is less than 4."; fi


declare -i n=0
declare -i m=0

echo
#WHILE-UNTIL loops
echo "---WHILE-UNTIL loops"
while (( n < 3 ))
do
	echo "n:$n"
	(( n++ ))
done
until (( m == 0)); do (( m++ )); sleep 1; done

echo
#For loops
echo "---FOR loops"
for i in {1..3}; do echo $i; done
for (( i=1; i<=3; i++)); do echo "The for is $i"; done

echo
#SWITCH-CASE 
echo "---SWITCH-CASE" animal="dog" 
case $animal in
	cat) echo "Feline";;
	dog|puppy) echo "Canine";;
	*) echo "No match!"
esac

echo
#FUNCTION
echo "---FUNCTION"
helloTher(){ echo "Hello $1 There $2"; }
helloTher Jerico Good

var1="VAR1"
numberthing(){
	echo "There was $# input in function"
	var2="VAR2"
	local var3="VAR3"
	declare -i i=1
	for f in $@
	do
		echo "$i: $f"
		(( i += 1 ))
	done
}
numberthing $(ls | grep .txt); echo
numberthing pine birch maple spruce
echo $var1; echo $var2; echo $var3	

echo
#Text to file
echo "---Text to file"
for i  in 1 2 3
do
	echo "This is line $i" > textfile.txt
done

while read f
	do echo "I read a line and it says: $f"
done < textfile.txt

echo
#READ input from user
echo -e "READ input from user\n\n"

read -p "Please write something: " name
#read -s pass
echo "User wrote: $name"

echo
#SELECT feature
echo
echo "Please choose one from the bellow:"
select animal in "cat" "dog" "bird" "fish" "quit"
do
	case $animal in
		cat|dog|bird|fish) echo "You selected $animal";;
		quit) break;;
		*) echo "I am not sure what is this.";;
	esac
done
