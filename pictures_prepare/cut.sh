#!/bin/bash


for i in {1..414}
do
	magick stoicism-$i.png -gravity South -chop 0x140 stoicism-$i.png
	magick stoicism-$i.png -gravity North -chop 0x80 stoicism-$i.png
	magick stoicism-$i.png -gravity West -chop 90x0 stoicism-$i.png
	magick stoicism-$i.png -gravity East -chop 90x0 stoicism-$i.png
done