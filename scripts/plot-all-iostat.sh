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
	echo "Plotting IO in $dir"
	base=$(basename $dir)
	echo "Basename : $base"
	outfile="$res/$base-iostat.ps"

	input_file="$dir/iostat-train-IOstat-parsed.txt"
	echo "Input file : $input_file"
	echo "Output file : $outfile \n"
	./doplot.sh $input_file $start_num $end_num $outfile 2


	echo "-------------------------------------------"

done
