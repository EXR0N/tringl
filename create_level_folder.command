#!/bin/bash

echo "Please enter the level data"

read data

cd levels

number="$(find * -maxdepth 0 -type d | wc -l)"
number=$(( $(( $number )) + 1 ))

mkdir $number
cd $number
pwd

echo $data > data.txt
cat data.txt

echo "created level $number!"
