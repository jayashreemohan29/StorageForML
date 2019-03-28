#!/bin/sh

for batch in 512; do
	numTh=16
	# Ensure top, iostat blktrace are not running
	sudo  kill $(pgrep blk)
	kill $(pgrep iostat)
	sudo kill $(pgrep iotop)
	kill $(pgrep top)
	#rm -rf *.log


	# Drop caches
	echo 3 | sudo tee /proc/sys/vm/drop_caches
	echo 'Start memory state'
	free -m

	#reset GPU
	sudo nvidia-smi --gpu-reset
	echo 'Start GPU state'
	nvidia-smi
	
	name="10pin-bsz-$batch-$numTh"
	outfile="10pin-out-bsz-$batch-$numTh.log"
	echo "Training with batch size $batch"
	python pytorch_imagenet.py --arch resnet50 -j $numTh --epochs 10 -b $batch --print-freq 1 --run $name ../datasets/ > $outfile 2>&1 

	#reset GPU
	sudo nvidia-smi --gpu-reset
	echo 'End GPU state'
	nvidia-smi
	
    	#dest="results/run-$name/"
	#mv *.log $dest
	#mv *.tar $dest
done 
