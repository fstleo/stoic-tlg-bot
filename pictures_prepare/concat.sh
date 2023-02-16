#!/bin/bash


for i in 36 68 102 138 139 140 172 206 238 272 273 274 310 342 380
do
	rm stoicism-$i.png
done

for i in 1 19 27 30 42 50 77 81 110 112 119 126 130 180 186 191 242 253 279 283 285 295 302 344 349 351 353 356 366 372 400 406 410
do
	magick convert stoicism-$i.png stoicism-$((i + 1)).png -append  stoicism-$i.png
	rm stoicism-$((i + 1)).png
done