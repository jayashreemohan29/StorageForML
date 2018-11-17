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
	echo "Plotting GPU util in $dir"
	base=$(basename $dir)
	echo "Basename : $base"
	outfile_mem="$res/$base-GPUmem.ps"
	outfile_util="$res/$base-GPUutil.ps"

	input_file="$dir/gpu-train-mem-parsed-combined.txt"
	if [ ! -f $input_file ]; then
		input_file="$dir/gpu-train-mem-parsed.txt"
	fi

	echo "Input file : $input_file"
	echo "Output file : $outfile_mem \n"
	./doplot.sh $input_file $start_num $end_num $outfile_mem 4


        input_file="$dir/gpu-train-util-parsed-combined.txt"
        if [ ! -f $input_file ]; then
                input_file="$dir/gpu-train-util-parsed.txt"
        fi

        echo "Input file : $input_file"
	echo "Output file : $outfile_util"
        ./doplot.sh $input_file $start_num $end_num $outfile_util 4

	echo "-------------------------------------------"

done
