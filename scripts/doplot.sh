#!/bin/sh

if [ "$#" -ne 5 ]; then
	echo "Usage : ./doplot.sh <input_file> <start-line-num> <end-line-num> <out-file.ps> <col-num>"
	exit 1
fi

in_file=$1
start_line=$2
end_line=$3
out_file=$4
column=$5
tmp_file="tmp.txt"


#First extract the given lines from input file
./extract_lines.sh $start_line $end_line $in_file $tmp_file

gnuplot -e "filename='$tmp_file';ofilename='$out_file';col=$column" plot.plt

#Plot col 1 against the col input, using these extracted points
