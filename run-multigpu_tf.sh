#!/bin/sh

for num_gpus in 4; do
	for batch in 256; do
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
		
		name="numg-$num_gpus-bsz-$batch-nvprof-convergence"
		outfile="out-numg-$num_gpus-bsz-$batch-nvprof-convergence.log"
		echo "Training with batch size $batch"
		PREFIX="/usr/local/cuda/bin/nvprof --profile-from-start off \
                --export-profile measurements/resnet50-tensorflow.nvprof -f --print-summary"
		$PREFIX python /mnt/ssd/StorageForML/tf_code/official/resnet/imagenet_main.py --data_dir=/mnt/ssd/datasets/ --batch_size=$batch --arg_run=$name --num_gpus=$num_gpus --datasets_num_parallel_batches=32 --stop_threshold=76  > $outfile 2>&1
	
		dest="/mnt/ssd/tf-runs/results/run-$name/"
		mv *.log $dest
		mv *.tar $dest
	done
done	
