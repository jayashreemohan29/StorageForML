#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Usage ./parse-cpu <path_to_result_dir> <trace_file_name>"
	exit 1
fi

rootdir=$1
tracefile=$2

for dir in $rootdir/*/; do
	echo "Parsing CPU files in $dir"
	outfile_mem="$dir/${tracefile%.*}-mem-parsed.txt"
	outfile_util="$dir/${tracefile%.*}-util-parsed.txt"

	input_file="$dir/$tracefile"
	echo "Input file : $input_file"

	# Idle%:8
	cat $input_file | grep "%Cpu" | awk -F' ' '{print $8 "\t" 100-$8 "\t"}' | awk '{print NR, "\t", $0}' > $outfile_util


	# 8: used mem by process, 10:mem used by buffer/cache , 4: total mem
	cat $input_file | grep "KiB Mem" | sed 's/\+/0 /g' | awk -F' ' '{print $8 "\t" $10 "\t" $4 "\t" $8/$4*100 "\t" ($8+$10)/$4*100 }' | awk '{print NR, "\t", $0}' > $outfile_mem
	#cat $input_file | grep P0 | awk -F' ' '{print $9 "\t" $11 "\t" $9/$11*100 }' | sed 's/MiB//g' | awk '{print NR, "\t", $0}' > $outfile_mem
	#cat $input_file | grep P0 | awk -F' ' '{print $13 "\t" 100 "\t" $13/100*100}' | sed 's/\%//g'| awk '{print NR, "\t", $0}' > $outfile_util
done
