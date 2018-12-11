#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import subprocess as sp
import os

def run(command):
    sp.call(command, shell=True)

#clone the respository
#cmd = "git clone https://github.com/jayashreemohan29/StorageForML.git"
#run(cmd)


cwd = os.getcwd()

#copy the datasets
#tars = [2]
#fromPath = "/mnt/1tbssd/vision/vision_data/ImageNet/CLS_LOC2014/image_train_tar/"
#toPath = "/mnt/ssd/datasets/"
#os.chdir(toPath)
#
#for i in tars:
#    cmd = "scp aastha@chennai.csres.utexas.edu:"+fromPath+"Tftar_"+str(i)+".tar.gz ."
#    print cmd
#    run(cmd)
#    cmd = "tar -xvzf "+toPath+"Tftar_"+str(i)+".tar.gz"
#    run(cmd)
#    cmd = "rm -rf "+toPath+"Tftar_"+str(i)+".tar.gz"
#    run(cmd)
##    if(i != len(tars)-1):
##	  #cmd = "mkdir /dev/shm/tar_bkp"
##	  #run(cmd)
##	  cmd = "mv "+toPath+"* /dev/shm/tar_bkp/."
##	  run(cmd)
#
##cmd = "mv /dev/shm/tar_bkp/* "+toPath+"."
##run(cmd)
#
#os.chdir(cwd)
#print(os.getcwd())

    
tf_code 
tf_code_dir = cwd+"/StorageForML/tf_code/"
tf_code_off_dir = cwd+"/StorageForML/tf_code/official"
os.chdir(tf_code_off_dir)

cmd = "export PYTHONPATH=$PYTHONPATH:"+tf_code_dir
run(cmd)


cmd = "sudo apt-get install python-pip"
run(cmd)
cmd = "pip install --user -r requirements.txt"
run(cmd)


#INSTALL ABSL & TENSORFLOW
#cmd = "pip install absl-py"
#run(cmd)
#cmd = "pip install tensorflow_gpu==1.5"
#run(cmd)

##SETUP LIBRARIES FOR TENSORFLOW
#cmd = "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64/"
#run(cmd)

#cmd = "sudo ln -s /usr/local/cuda/lib64/libcublas.so.9.1 /usr/local/cuda/lib64/libcublas.so.9.0"
#run(cmd)

#cmd = "sudo ln -s /usr/local/cuda/lib64/libcusolver.so.9.1 /usr/local/cuda/lib64/libcusolver.so.9.0"
#run(cmd)

#cmd = "sudo ln -s /usr/local/cuda/lib64/libcudart.so.9.1 /usr/local/cuda/lib64/libcudart.so.9.0"
#run(cmd)

#cmd = "sudo ln -s /usr/local/cuda/lib64/libcufft.so.9.1 /usr/local/cuda/lib64/libcufft.so.9.0"
#run(cmd)

#cmd = "sudo ln -s /usr/local/cuda/lib64/libcurand.so.9.1 /usr/local/cuda/lib64/libcurand.so.9.0"
#run(cmd)


# INSTALL CUDA 9.0
#cuda_dir = "cuda_90_install"
#cmd = "mkdir "+cuda_dir
#run(cmd)
#os.chdir(cwd+"/"+cuda_dir)
#print(os.getcwd())
#
#cmd = "wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run"
#run(cmd)
#cmd = "chmod +x cuda_9.0.176_384.81_linux-run"
#run(cmd)
#cmd = "./cuda_9.0.176_384.81_linux-run --extract="+os.getcwd()
#run(cmd)
#cmd = "sudo ./cuda-linux.9.0.176-22781540.run"
#run(cmd)
#cmd = "sudo bash -c \"echo /usr/local/cuda/lib64/ > /etc/ld.so.conf.d/cuda.conf\"; sudo ldconfig"
#run(cmd)
#os.chdir(cwd)

#CUDNN GET DEB FILES
#fromPath = "/mnt/1tbssd/cudnnLibs"
#cmd = "mkdir cudnnLibs"
#run(cmd)
#toPath = cwd+"/cudnnLibs"
#os.chdir(toPath)
#cmd  = "scp aastha@chennai.csres.utexas.edu:"+fromPath+"/* ."
#run(cmd)
#cmd = "sudo dpkg -i libcudnn7_7.4.1.5-1+cuda9.0_amd64.deb"
#run(cmd)
#cmd = "sudo dpkg -i libcudnn7-dev_7.4.1.5-1+cuda9.0_amd64.deb"
#run(cmd)
#cmd = "sudo dpkg -i libcudnn7-doc_7.4.1.5-1+cuda9.0_amd64.deb"
#run(cmd)
#os.chdir(cwd)

#INSTALL STAT REQ

cmd = "sudo apt-get install iostat"
run(cmd)
cmd = "sudo apt-get install blktrace"
run(cmd)
cmd = "sudo apt-get install iotop"
run(cmd)
