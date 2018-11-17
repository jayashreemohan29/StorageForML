#!/bin/sh

if [ "$#" -ne 3 ]; then
	echo "Usage ./plot-all <path_to_result_dir> <start_line_num> <end_line_num>"
	exit 1
fi

rootdir=$1
start_num=$2
end_num=$3

res="../graphs/$(basename $rootdir)"

if [ ! -d $res ]; then
	mkdir -p $res
fi

for dir in $rootdir/*/; do
	echo "-------------------------------------------"
	echo "Plotting CPU util in $dir"
	base=$(basename $dir)
	echo "Basename : $base"
	outfile_mem="$res/$base-CPUmem.ps"
	outfile_util="$res/$base-CPUutil.ps"

	input_file="$dir/top-train-mem-parsed.txt"
	echo "Input file : $input_file"
	echo "Output file : $outfile_mem \n"
	./doplot.sh $input_file $start_num $end_num $outfile_mem 6


        input_file="$dir/top-train-util-parsed.txt"
        echo "Input file : $input_file"
	echo "Output file : $outfile_util"
        ./doplot.sh $input_file $start_num $end_num $outfile_util 3

	echo "-------------------------------------------"

done
