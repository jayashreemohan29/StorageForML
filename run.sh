#!/bin/sh

# Ensure top, iostat blktrace are not running
sudo  kill $(pgrep blk)
kill $(pgrep iostat)
kill $(pgrep top)
rm -rf *.log


# Drop caches
echo 3 | sudo tee /proc/sys/vm/drop_caches
echo 'Start memory state'
free -m

#reset GPU
sudo nvidia-smi -i 0 --gpu-reset
echo 'Start GPU state'
nvidia-smi -i 0

#Let's run the code
for batch in 16 32 64 128 256; do
	name="bsz-$batch"
	outfile="out-bsz-$batch.log"
	echo "Training with batch size $batch"
	python pytorch_imagenet.py --arch resnet50 -j 4 --epochs 1 -b $batch --print-freq 1 --gpu 0 --run $name ../dataset/imagenet/ > $outfile 2>&1
done 

dest="/dev/shm/results/run-$name/"
mv *.log dest
