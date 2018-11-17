#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Usage ./parse-gpu <path_to_result_dir> <trace_file_name>"
	exit 1
fi

rootdir=$1
tracefile=$2

for dir in $rootdir/*/; do
	echo "Parsing GPU files in $dir"
	outfile_mem="$dir/${tracefile%.*}-mem-parsed.txt"
	outfile_util="$dir/${tracefile%.*}-util-parsed.txt"

	input_file="$dir/$tracefile"
	echo "Input file : $input_file"
	cat $input_file | grep P0 | awk -F' ' '{print $9 "\t" $11 "\t" $9/$11 }' | sed 's/MiB//g' | awk '{print NR, "\t", $0}' > $outfile_mem
	cat $input_file | grep P0 | awk -F' ' '{print $13}' | sed 's/\%//g'| awk '{print NR, "\t", $0}' > $outfile_util

	#Let's get the available memory
	mem=$(($(awk 'NR==1{print $3}' $outfile_mem) * 2))
	echo "Max mem = $mem"

	echo "Now combining files"
	./combineGPUresult.sh $outfile_mem $mem
	./combineGPUresult.sh $outfile_util 200
	
done
