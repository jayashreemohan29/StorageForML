#!/bin/sh

if [ "$#" -ne 4 ]; then
	echo "Enter start and end line number <i/p file> <o/p file>"
	exit 1
fi

start=$1
end=$2
char="p"
endp="$end$char"
file=$3
outfile=$4

sed -n $start,$endp $file > $outfile
