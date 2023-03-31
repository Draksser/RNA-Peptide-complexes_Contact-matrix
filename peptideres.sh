#! /bin/bash

grep ATOM peptide.pdb > peptide_clean.pdb
sed -i '/REMARK/d' peptide_clean.pdb
sed -i '/SOURCE/d' peptide_clean.pdb
sed -i '/KEYWDS/d' peptide_clean.pdb
sed -i '/JRNL/d' peptide_clean.pdb
sed -i 's/\ \ */\ /g' peptide_clean.pdb
sed -i 's/ /;/g' peptide_clean.pdb

######## THIS STEP IS EDITABLE #################################
cat peptide_clean.pdb | cut -d ';' -f 4,6 > finalpeptide.pdb
################################################################

rm peptide.pdb
rm peptide_clean.pdb
mv finalpeptide.pdb finalpeptide.txt
sed -i 's/;//g' finalpeptide.txt
uniq finalpeptide.txt peptideres.txt
rm finalpeptide.txt

