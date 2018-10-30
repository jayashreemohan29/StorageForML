universe = vanilla
Initialdir = /scratch/cluster/aastha/thesis/
Executable = /lusr/bin/bash
Arguments = /scratch/cluster/aastha/thesis/task.sh
+Group   = "GRAD"
+Project = "INSTRUCTIONAL"
+ProjectDescription = "MS Thesis Experiment"
Requirements = TARGET.GPUSlot
getenv = True
request_GPUs = 1
+GPUJob = true
Log =  /scratch/cluster/aastha/thesis/condor.log
Error =  /scratch/cluster/aastha/thesis/condor.err
Output =  /scratch/cluster/aastha/thesis/condor.out
Notification = complete
Notify_user = aastha@cs.utexas.edu
Queue 1
