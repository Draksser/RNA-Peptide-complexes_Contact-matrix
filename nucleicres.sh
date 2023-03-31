#! /bin/bash

grep ATOM nucleic.pdb > nucleic_clean.pdb
sed -i '/REMARK/d' nucleic_clean.pdb
sed -i '/SOURCE/d' nucleic_clean.pdb
sed -i '/KEYWDS/d' nucleic_clean.pdb
sed -i '/JRNL/d' nucleic_clean.pdb
sed -i 's/\ \ */\ /g' nucleic_clean.pdb
sed -i 's/ /;/g' nucleic_clean.pdb

######## THIS STEP IS EDITABLE #################################
cat nucleic_clean.pdb | cut -d ';' -f 4,6 > finalnucleic.pdb
################################################################

rm nucleic.pdb
rm nucleic_clean.pdb
mv finalnucleic.pdb finalnucleic.txt
sed -i 's/;//g' finalnucleic.txt


uniq finalnucleic.txt nucleicres.txt
rm finalnucleic.txt

