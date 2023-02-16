#!/bin/bash

for i in {1..413}
do
	if [[ ! -f stoicism-$i.png ]]
	then
		echo "$i doesn't exist"
		j=$((i+1))
		while [[ $j -lt 413 ]]
		do 
			
			if [[ -f stoicism-$j.png ]]
			then
				mv stoicism-$j.png stoicism-$i.png
				echo "rename stoicism-$j to stoicism-$i"
				break
			fi
			((j++))
		done
	fi
done


