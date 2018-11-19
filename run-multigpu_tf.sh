#!/bin/sh

for batch in 16 32 256; do
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
	nvidia-smi -i 0
	
	name="bsz-$batch"
	outfile="out-bsz-$batch.log"
	echo "Training with batch size $batch"
	python imagenet_main.py $batch $name --data_dir=../dataset/imagenet/ > $outfile 2>&1

	dest="/dev/shm/results/run-$name/"
	mv *.log $dest
	mv *.tar $dest
done 
