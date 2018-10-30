universe = vanilla
Initialdir = /scratch/cluster/aastha/thesis/StorageForML 
Executable = /lusr/bin/bash
Arguments = /scratch/cluster/aastha/thesis/StorageForML/condor/task_pyt.sh
+Group   = "GRAD"
+Project = "INSTRUCTIONAL"
+ProjectDescription = "MS Thesis Experiment"
Requirements = TARGET.GPUSlot
getenv = True
request_GPUs = 1
+GPUJob = true
Log =  /scratch/cluster/aastha/thesis/StorageForML/logs/condor_pyt.log
Error =  /scratch/cluster/aastha/thesis/StorageForML/logs/condor_pyt.err
Output =  /scratch/cluster/aastha/thesis/StorageForML/logs/condor_pyt.out
Notification = complete
Notify_user = aastha@cs.utexas.edu
Queue 1
