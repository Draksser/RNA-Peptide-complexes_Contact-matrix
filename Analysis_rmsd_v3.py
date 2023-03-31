#! /usr/bin/python3

#Verify the gro file ==> Nucleic molecule must be before Peptide

import subprocess
import os
import time
import shutil

print("RMSD Calculations for RNA-Peptide complexes ! \n\n First step : create an index file with only 3 groups : RNA, Peptide and complex \n For that, you need to specify the number of nucleotides of your RNA, the number of residues of your peptide and the input file (usually .gro file) to feed gmx make_ndx command")

X = int(input("Number of RNA nucleotides = "))
Y = int(input("Number of peptidic residues = "))
file = input("Name of the input file (.gro or other) = ")

print("\nSecond step : RMSD calculations with the help of the index file previously generated \n --> RMSD peptide fit to peptide (peptide deformation) \n --> RMSD RNA fit to RNA (RNA deformation) \n --> RMSD Complex fit to complex (Complex Deformation) \n --> RMSD peptide fit to RNA (peptide movement) \n --> RMSD RNA fit to peptide (RNA movement) \nFor that, you need to specify the trajectory file of your production run (.tpr), and the topology file in binary (.tpr).")

traj = input("Trajectory file name (.xtc) = ")
top = input("Topology file name (.tpr) = ")


###############################################################################
# FIRST STEP : Create an index file with RNA, Peptide, and the complex
###############################################################################


#Define some variables
instructions_sp = list()
instructions_sp.append("keep0")


#Create the instruction_sp file to feed gmx make_ndx
instructions_sp.append("ri1-{}".format(str(X)))
instructions_sp.append("ri{}-{}".format(str(X+1), str(X+Y)))
instructions_sp.append("name1 RNA")
instructions_sp.append("name2 Peptide")
instructions_sp.append("1 | 2")
instructions_sp.append("name3 Complex")
instructions_sp.append("q")

with open('instructions_sp.txt', 'w+') as f :
   for items in instructions_sp :
      f.write('%s\n' %items)
   print("Instructions written successfully !")
f.close()

#Execute gmx make_ndx with the instruction file
subprocess.run(["gmx make_ndx -f {} -o index_rms.ndx < instructions_sp.txt".format(file)], shell = True)

#Remove temporary files
os.remove("instructions_sp.txt")

print("Index file for rmsd calculations successfully created !")

###############################################################################
# SECOND STEP : Calculate RMSD 
###############################################################################

#Run gmx rms command
RMSD1 = subprocess.run(["echo 1 1 | gmx rms -f {} -s {} -n index_rms.ndx -o rmsd_n_fit_to_n.xvg -tu ns".format(traj, top)], shell = True)
time.sleep(1)
RMSD2 = subprocess.run(["echo 2 2 | gmx rms -f {} -s {} -n index_rms.ndx -o rmsd_p_fit_to_p.xvg -tu ns".format(traj, top)], shell = True)
time.sleep(1)
RMSD3 = subprocess.run(["echo 3 3 | gmx rms -f {} -s {} -n index_rms.ndx -o rmsd_c_fit_to_c.xvg -tu ns".format(traj, top)], shell = True)
time.sleep(1)
RMSD4 = subprocess.run(["echo 1 2 | gmx rms -f {} -s {} -n index_rms.ndx -o rmsd_p_fit_to_n.xvg -tu ns".format(traj, top)], shell = True)
time.sleep(1)
RMSD5 = subprocess.run(["echo 2 1 | gmx rms -f {} -s {} -n index_rms.ndx -o rmsd_n_fit_to_p.xvg -tu ns".format(traj, top)], shell = True)
time.sleep(1)

#Now create an xvg file with all the RMSDs

label = subprocess.run(["./add_label_rmsd.sh"], shell = True)

#Now create a directory to store RMSD files
os.mkdir("analysis_rms")
path = os.getcwd()
dest = path + '/analysis_rms'
print(dest)

rmsd_files = os.listdir()

for rf in rmsd_files :
   if rf.startswith("rmsd") :
      shutil.move(rf, dest)
      print("RMSD file successfully moved to 'analysis_rms' directory")
   else :
      print("OTHER")

print("\n\n ANALYSIS - RMSD CALCULATIONS COMPLETED !")









