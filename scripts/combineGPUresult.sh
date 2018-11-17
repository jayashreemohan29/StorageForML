#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Requires input file and max of the value being combined"
	exit 1
fi

input_file=$1
max_v=$2
out_file="${input_file%.*}-combined.txt"

echo "Combined out file =  $out_file with max = $max_v"

# Get the second column (memory/GPU util) from every two consecutive lines of the file, 
# This is assuming we have 2 GPUs
# Add them up, and using the max value of mem( or util),  compute % utilization

cat $input_file | awk -F' ' '{print $2}' | awk -v c="$max_v" '{a=$0;getline;b=$1; print a+b "\t" c "\t" (a+b)/c*100 "\t"}'| awk '{print NR, "\t", $0}'  > $out_file
