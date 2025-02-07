Step 0: On CNAF, have directories args, log, data, lists, output each with a subdirectory labelling the dataset, say "ds3607" in each of them (unfortunately I don't have things set up to generate directories yet, this should be implemented at some point). There then are the files "MakeArgFiles.py", and whatever analysis macro you have, and startJob_reduced.sh (which is the bash script that will be run for each job-it's what tells the working nodes to run the macro) in this case "MakeReducedMulitiplicityFiles.C"

Step 1: on ULITE, call 
$ GetRunInfo -d DATASET -S -H
where DATASET is the dataset in question, for all that follows we'll take it to be 3607. The return should be something like:
 Dataset |  Run   |      Run Type      |         Start Time         |         Stop Time          | Run Time | Stop Status
 ------- + ------ + ------------------ + -------------------------- + -------------------------- + -------- + -----------
  3607   | 302577 | Setup_WorkingPoint | May 02, 2019 06:24:32+0000 | May 02, 2019 09:31:27+0000 | 3:06:55  |   OK (0)   
  3607   | 302595 | Setup_WorkingPoint | May 08, 2019 07:39:22+0000 | May 08, 2019 10:46:52+0000 | 3:07:30  |   OK (0)   
  3607   | 302614 | Setup_WorkingPoint | May 19, 2019 12:12:54+0000 | May 19, 2019 15:19:59+0000 | 3:07:05  |   OK (0)   
  3607   | 302627 | Setup_WorkingPoint | May 23, 2019 17:06:22+0000 | May 23, 2019 20:13:42+0000 | 3:07:20  |   OK (0)   
  3607   | 302635 | Setup_WorkingPoint | May 30, 2019 09:58:57+0000 | May 30, 2019 13:05:52+0000 | 3:06:55  |   OK (0)   
  3607   | 302646 | Setup_WorkingPoint | Jun 06, 2019 10:04:19+0000 | Jun 06, 2019 13:11:24+0000 | 3:07:05  |   OK (0)   
  3607   | 302657 | Setup_WorkingPoint | Jun 13, 2019 08:25:31+0000 | Jun 13, 2019 11:32:36+0000 | 3:07:05  |   OK (0)   
  3607   | 302668 | Setup_WorkingPoint | Jun 20, 2019 10:05:59+0000 | Jun 20, 2019 13:13:54+0000 | 3:07:55  |   OK (0)   
  3607   | 302678 | Setup_WorkingPoint | Jun 27, 2019 09:55:15+0000 | Jun 27, 2019 13:02:15+0000 | 3:07:00  |   OK (0)   
  3607   | 302703 | Setup_WorkingPoint | Jul 10, 2019 04:23:42+0000 | Jul 10, 2019 07:31:07+0000 | 3:07:25  |   OK (0)   
  3607   | 350604 |    Calibration     | May 02, 2019 14:09:54+0000 | May 03, 2019 14:00:23+0000 | 23:50:29 |   OK (0)   
  3607   | 350605 |    Calibration     | May 03, 2019 14:04:41+0000 | May 04, 2019 14:18:15+0000 | 24:13:34 |   OK (0) 
  ....
  
Copy this, and put it in "data" as ds3607.dat (or replacing the dataset with it's own #).
  
Step 2:
Ensure that the directory "heredir" in the file MakeArgFiles.py corresponds to where you are working as it currently uses my directory. Then call 
$python MakeArgFiles.py 3607
So long as everything is in order, this will populate args/ds3607 with all the argument files corresponding to the different runs in ds3607 (note: as currently configured, only bgd and calib runs are considered and labelled as such), along with all the list files. It will also generate ds3607_submitter_calib and ds3607_submitter_bgd which are the respective submission files for the calib and bgd runs.

Step 3: run
$condor_submit -name sn-01 -spool ds3607_submitter_bgd
So condor is weird: in this case, we need to call the name of the condor engine or whatever, sn-01, to be able to talk to it or such. We then use the -spool JOB_NAME to submit the jobs. Taking a look at ds3607_submitter_bgd, we see:

Universe = vanilla
Executable = startJob_reduced.sh
Output = /storage/gpfs_data/cuore/users/dmayer/PamelaUROP/log/out.$(process)
Error = /storage/gpfs_data/cuore/users/dmayer/PamelaUROP/log/err.$(process)
Log = /storage/gpfs_data/cuore/users/dmayer/PamelaUROP/log/log.$(process)
transfer_input_files = $(filename)
Arguments = $(filename)
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
queue filename matching files args/ds3607/*bgd*.dat

Some of these variables I don't really understand, but the thing that matters here is the "queue filename matching files args/ds3607/*bgd*.dat", as this will go through said directory and submit a job of the form startJob_reduced.sh, and then from there the bash script takes the filename as an input and will run.

Step 4: This should launch the jobs! They can be monitored via:
$condor_q -name sn-01 JOB_ID
where JOB_ID is given by the submission. I don't know how to queury it after submission, so write it down or such!
And I'm pretty sure condor_rm can be used to kill jobs, but you might want to check that one.
Also, condor doesn't automatically transfer log info, so do to that for debugging you need to call
$condor_transfer_data -name sn-01 JOB_ID
Also, when you submit jobs as a group they will be assigned JOB_ID.sub_id where sub_id goes from 0 to (the number of jobs-1) and can be monitored individually as such, and JOB_ID.* will include all of them.
