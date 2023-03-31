#! /usr/bin/python3

import os
import time
import subprocess
import shutil
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice
import matplotlib.ticker as plticker


print("Analysis : Contact matrix of an RNA-peptide complex using gromacs mindist function \n Make sure that every bash script is present in your working directory \n The scripts are : \n --> Colum_NX_NY.sh \n --> nucleicres.sh \n --> peptideres.sh")

#Insructions 1 :
print("\nFIRST STEP : let's create our index file with each nucleotide from our RNA and each residues from our peptide. WARNING, the RNA MUST be before the peptide in your gro file (or other input file of your convenience), otherwise it won't work.")

X = int(input("Number of nucleotides = "))
Y = int(input("Number of peptidic residues = "))
filegro = input("Name of the input file (usually .gro) = ")


#Instructions 2 :
print("\nSECOND STEP : we're going to calculate minimum distance between each residue-nucleotide pair. For that, we need the number of peptide residues and RNA nucleotides, but also a trajectory file from your production run (.xtc), with the topology file in binary (.tpr) \n Verify the gro (or other accepted format) file !!! ==> Nucleic molecule must be before Peptide !!!")

traj = input("trajectory file name (.xtc) = ") 		# "complex.xtc"
top = input("topology file name (.tpr) = ")    		# "complex.tpr"

#Instructions 3 :
print("\nTHIRD STEP : this step is about extracting the average values of minimum distance between each nucleotide-residue pair, to store them in a temporary file")
time.sleep(3)

#Instructions 4 :
print("\nLAST STEP : Contact Matrix v3 for RNA-Peptide complexes \n Files needed are : \n --> Peptide pdb file \n --> Nucleic pdb file")

namePeptide = input( "Name of the peptide : ")
Peptidefile = input( "Name of the peptide pdb file : ")
nameRNA = input( "Name of the RNA : ")
RNAfile = input( "Name of the RNA pdb file : ")




#-------------------------------------------------------------------------------------------------------------------------------------------------
# FIRST STEP : create an index file with all nucleotides from the RNA and all residus from the peptide
#-------------------------------------------------------------------------------------------------------------------------------------------------

#Define some variables
instructions = list()
instructions.append("keep0")


#Create the instruction file to feed gmx make_ndx
for i in range(1, X+1) :
   instructions.append("ri" + str(i))
for j in range(X+1, X+Y+1) :
   instructions.append("ri" + str(j))
for k in range(1, X+1) :
   instructions.append("name{} N{}".format(str(k), str(k)))
for l in range(X+1, X+Y+1) :
   instructions.append("name{} P{}".format(str(l), str(l-X)))
instructions.append("q")

with open('instructions.txt', 'w+') as ins :
   for items in instructions :
      ins.write('%s\n' %items)
   print("Instructions written successfully !")
ins.close()

#Execute gmx make_ndx with the instruction file
subprocess.run(["gmx make_ndx -f {} -o res_index.ndx < instructions.txt".format(filegro)], shell = True)

#Remove temporary files
os.remove("instructions.txt")

print("Index file with residues successfully created !")


#-------------------------------------------------------------------------------------------------------------------------------------------------
# SECOND STEP : Calculate minimum distance between each nucleotide-residue pair using gmx mindist
#-------------------------------------------------------------------------------------------------------------------------------------------------


#Mindist loop for each combination [NX_PY]
for N in range(1,X+1):
  for P in range(1,Y+1):
    subprocess.run(["echo N{} P{} | gmx mindist -f {} -s {} -n res_index.ndx -od dist_N{}_P{}.xvg -tu ns".format(str(N), str(P), traj, top, str(N), str(P))], shell = True)

print("Distances files successfully generated")


#-------------------------------------------------------------------------------------------------------------------------------------------------
# THIRD STEP : Extract the average minimum distance for each nucleotide-residue pair and store them in a temporary file
#-------------------------------------------------------------------------------------------------------------------------------------------------

#Define variable for storing data
store = list() 
tab = []

#N and P variables were used before, so we need to 'reset'them
def reset(var) :
   return type(var)()
reset(N)
reset(P)

#Start the loop in the loop #inception
for N in range(1,X+1):
  for P in range(1,Y+1):


    #Take distance file one by one and rename it to dist_NX_PY.xvg
    shutil.copyfile('dist_N{}_P{}.xvg'.format(str(N), str(P)), 'dist_NX_PY.xvg')   



    #Execute bash script "Column_NX_NY.sh" to get a file named "final_NX_PY.txt" with distance values organised in a column
    subprocess.call('./Column_NX_NY.sh')


    #Define some variables
    li = list()
    S = 0
    average = 0 
    


    #Extract average value
    with open("final_NX_PY.txt") as fileNXPY:
       for lign in fileNXPY :
         lign = lign.strip()
         li.append(float(lign))

    S = sum(li)

    average = S / int(len(li))

    a= "av_N{}_P{} = ".format(str(N), str(P)) + str(average)
    print(a)



    #Remove temporary files
    os.remove("final_NX_PY.txt")
    os.remove("dist_NX_PY.xvg")



    #Store average values
    store.append(a)
    tab.append(float(average)) 



#Organize average values correctly


store.append("Max = " + str(max(tab)))
store.append("Min = " + str(min(tab)))


#Create output files with collected data
with open('Averages.txt', 'w+') as fav:
   for items2 in store :
      fav.write('%s\n' %items2)
   print("File written successfully")
fav.close()

with open('Averages_num.txt', 'w+') as fav2:
   for items3 in tab :
      fav2.write('%s\n' %items3)
   print("File written successfully")
fav2.close()

#Now create a directory to store distances files
os.mkdir("mindist")
path = os.getcwd()
dest = path + '/mindist'
print(dest)

dist_files = os.listdir()

for df in dist_files :
   if df.startswith("dist") :
      shutil.move(df, dest)
      print("Distances file successfully moved to 'mindist' directory")
   else :
      print("OTHER")


#-------------------------------------------------------------------------------------------------------------------------------------------------
# LAST STEP : Build the contact matrix using matplotlib
#-------------------------------------------------------------------------------------------------------------------------------------------------

#Define some variables
file = 'Averages_num.txt'
Input = list()

#Nucleotide residue names
nres = list()
shutil.copyfile(RNAfile, 'nucleic.pdb')
subprocess.call('./nucleicres.sh')
nf = open('nucleicres.txt', 'r')
for n in nf :
    nres.append(str(n.rstrip()))

#Peptidic residue names
pres = list()
shutil.copyfile(Peptidefile, 'peptide.pdb')
subprocess.call('./peptideres.sh')
pf = open('peptideres.txt', 'r')
for p in pf :
    pres.append(str(p.rstrip()))

#Collect data from averages file to create a list (Input)
f = open(file, 'r')
for line in f :
   Input.append(float(line.rstrip()))


#Divide the list to form a list of list (Output)
split = [len(Input)//X]*X
lst = iter(Input)
Output = [list(islice(lst, elem))
	for elem in split]


#Convert the output into an array
matrix = np.array(Output)


#Prepare xticks and yticks
y = [o for o in range(0, X)]
x = [p for p in range(0, Y)]


#Construct the contact matrix
fig, ax = plt.subplots()
im = ax.imshow(matrix, origin= 'lower', cmap ='RdBu')
plt.colorbar(im).set_label(label = 'Distances (nm)', weight='bold')

#Add legend and titles
plt.title('Contact Matrix : {}-{} complex'.format(namePeptide, nameRNA), fontweight = 'bold')
plt.xlabel(namePeptide + ' peptide', weight = 'bold')
plt.ylabel(nameRNA + ' RNA', weight = 'bold')


#Modify xticks and yticks
plt.yticks(y)
plt.xticks(x)
ax.set_yticklabels(nres, fontsize = 6)
ax.set_xticklabels(pres, fontsize = 6, rotation = 90)


plt.savefig('contact_matrix_{}-{}_complex.pdf'.format(namePeptide, nameRNA), format='pdf')

os.remove('peptideres.txt')
os.remove('nucleicres.txt')
os.remove('Averages_num.txt')

print("\nANALYSIS COMPLETED !")

