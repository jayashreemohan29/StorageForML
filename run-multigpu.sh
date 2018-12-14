#!/bin/sh

for batch in 512; do
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
	
	name="bsz-$batch"
	outfile="out-bsz-$batch.log"
	echo "Training with batch size $batch"
	python3 pytorch_imagenet.py --arch resnet50 -j 32 --epochs 1 -b $batch --print-freq 1 --run $name ../dataset/imagenet/ > $outfile 2>&1

	#reset GPU
	sudo nvidia-smi --gpu-reset
	echo 'End GPU state'
	nvidia-smi
	
    dest="/dev/shm/results/run-$name/"
	mv *.log $dest
	mv *.tar $dest
done 
