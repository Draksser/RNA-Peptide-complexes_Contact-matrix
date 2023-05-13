# RNA-Peptide-complexes_Contact-matrix

This python script is designed to build a contact matrix of an RNA-peptide complex using gromacs mindist function. For this, you have to make sure that every bash script is present in your working directory.
The scripts are : 
  --> Colum_NX_NY.sh 
  --> nucleicres.sh 
  --> peptideres.sh

Several additional python modules are required for this scriipt to function, please make sure all of these are installed : 
- Subprocess
- NumPy
- Shutil
- Matplotlib
- itertools

You will have to provide some information about the peptide and the RNA of the complex, allong with certain files :
- Number of nucleotide of your RNA
- Name of the RNA
- Number of peptide residues
- Name of the peptide
- PDB file of the RNA alone
- PDB file of the peptide alone
- Input file to create an index file (usally gro file)
- Trajectory file of your production run, preferably without periodic boundary conditions (.xtc)
- Topology file of your production run in binary (.tpr)

**==> First step : creating an index file**

The index file is created using gmx make_ndx command using the input file (.gro), the output file is named 'res_index.ndx'.
It uses the 'for...in' loop inside an other one.
The index file created with this script contains all nucleotides of the RNA named N1 to NX, X being the number of nucleotides, allong with all peptide residues named P1 to PY, Y being the number of residues.

**==> Second step : calculating every minimum distance between each residue-nucleotide pair**

The minimum distance is calculated using gmx mindist command using xtc, tpr and the index file (.ndx) created previously.
Knowing that there is X nucleotides for the RNA and Y residues for the peptide, there is X 	&times; Y combinations, so there is X &times; Y minimum distances to calculate. This step can take a very long time, especially if your using this script for an All-Atom (AA) simulation.

**==> Third step : Calculating the average value for each minimum distance**

For that, the python script will call the 'Colum_NX_NY.sh' bash script, which extract each minimium distance of the corresponding xvg file and store it in a temporary file called 'dist_NX_PY.txt'
The python script will then use this txt file to create a list, with which it will calculate the average minimum distance value. Each average value will then be stored in a python list.

**==> Last step : building the contact matrix***

The python list containing each average minimumm distance value will be converted to an NumPy array, that will be used to build the contact matrix using imshow function from Matplotlib. The residue names of the peptide and nucleotide names of the RNA will be extracted from the corresponding pdb files using 'nucleicres.sh' and 'peptideres.sh' respectively, and will be used to modify the tick labels of the matrix. These two bash scripts will be called by the python script. 

# RNA-Peptide-complexes_RMSD_calculations

The second python script calculates 5 different RMSDs for the RNA-peptide complex, using the initial coordinates of the peptide and the RNA with the gmx rms command.


