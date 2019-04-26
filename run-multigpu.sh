#!/bin/sh

mem=$1
for batch in 128 256 512; do
	for numTh in 0 4 8 16 32; do
	       for numGPU in 1 2 4; do
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
			
			name="BigD-Epochs-3-Mem-$mem-Bsz-$batch-Th-$numTh-GPUs-$numGPU"
			outfile="results/BigD-Epochs-3-out-Mem-$mem-Bsz-$batch-Th-$numTh-GPUs-$numGPU.log"
			echo "Training with batch size $batch"
			/usr/bin/time -v python3 pytorch_imagenet.py --arch resnet50 -j $numTh --epochs 3 -b $batch --print-freq 1 --run $name --numGPUs $numGPU ../datasets/ > $outfile 2>&1 

			#reset GPU
			sudo nvidia-smi --gpu-reset
			echo 'End GPU state'
			nvidia-smi
			
    			#dest="results/run-$name/"
			#mv *.log $dest
			#mv *.tar $dest
		done
	done
done 
