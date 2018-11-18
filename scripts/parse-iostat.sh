#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Usage ./parse-cpu <path_to_result_dir> <trace_file_name>"
	exit 1
fi

rootdir=$1
tracefile=$2

for dir in $rootdir/*/; do
	echo "Parsing IO files in $dir"
	outfile="$dir/${tracefile%.*}-IOstat-parsed.txt"

	input_file="$dir/$tracefile"
	echo "Input file : $input_file"

	# 3 : Disk IO throughput
	cat $input_file | grep "sda1" | awk -F' ' '{print $5/1024}' | awk '{print NR, "\t", $0}' > $outfile


	#cat $input_file | grep P0 | awk -F' ' '{print $9 "\t" $11 "\t" $9/$11*100 }' | sed 's/MiB//g' | awk '{print NR, "\t", $0}' > $outfile_mem
	#cat $input_file | grep P0 | awk -F' ' '{print $13 "\t" 100 "\t" $13/100*100}' | sed 's/\%//g'| awk '{print NR, "\t", $0}' > $outfile_util
done
