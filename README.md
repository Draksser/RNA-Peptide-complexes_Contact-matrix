# RNA-Peptide-complexes_Contact-matrix

This python script is designed to build a contact matrix of an RNA-peptide complex using gromacs mindist function. For this, you have make sure that every bash script is present in your working directory.
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
- PDB file of the RNA
- PDB file of the peptide
- Input file to create an index file (usally gro file)
- Trajectory file of your production run, preferably without periodic boundary conditions (.xtc)
- Topology file of your production run in binary (.tpr)

**==> First step : creating an index file**
The index file is created using gmx make_ndx command using the input file (.gro), the output file is named 'res_index.ndx'.
It uses the 'for...in' loop inside an other one.
The index file created with this script contains all nucleotides of the RNA named N1 to NX, X being the number of nucleotides, allong with all peptide residues named P1 to PY, Y being the number of residues.

**==> Second step : Calculating every minimum distance between each residue-nucleotide pair**
The minimum distance is calculated using gmx mindist command using xtc, tpr and the index file (.ndx) created previously.
Knowing that there is X nucleotides for the RNA and Y residues for the peptide, there is X 	&times; Y combinations, so there is X &times; Y minimum distances to calculate.


