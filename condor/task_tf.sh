#!/usr/bin/env bash

export PYTHONPATH="$PYTHONPATH:/scratch/cluster/aastha/thesis/models"
python  /scratch/cluster/aastha/thesis/models/official/resnet/imagenet_main.py --data_dir=/scratch/cluster/aastha/thesis/data/tiny-imagenet-200
