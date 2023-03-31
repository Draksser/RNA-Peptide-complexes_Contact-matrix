#! /bin/bash

cp rmsd_c_fit_to_c.xvg c_c.xvg
cp rmsd_n_fit_to_n.xvg n_n.xvg
cp rmsd_n_fit_to_p.xvg n_p.xvg
cp rmsd_p_fit_to_n.xvg p_n.xvg
cp rmsd_p_fit_to_p.xvg p_p.xvg

sed -i -e '/#/d' -e '/@/d' c_c.xvg
sed -i -e '/#/d' -e '/@/d' n_n.xvg
sed -i -e '/#/d' -e '/@/d' n_p.xvg
sed -i -e '/#/d' -e '/@/d' p_n.xvg
sed -i -e '/#/d' -e '/@/d' p_p.xvg


sed -i '1i@    title "RMSD"\n@    xaxis  label "Time (ns)"\n@    yaxis  label "RMSD (nm)"\n@TYPE xy\n@    s0 legend  "Complex fit to Complex"' c_c.xvg
sed -i '1i@    s1 legend  "RNA fit to RNA"' n_n.xvg
sed -i '1i@    s2 legend  "RNA fit to Peptide"' n_p.xvg
sed -i '1i@    s3 legend  "Peptide fit to RNA"' p_n.xvg
sed -i '1i@    s4 legend  "Peptide fit to Peptide"' p_p.xvg

cat c_c.xvg n_n.xvg n_p.xvg p_n.xvg p_p.xvg > rmsd_total.xvg

rm c_c.xvg
rm n_n.xvg
rm n_p.xvg
rm p_n.xvg
rm p_p.xvg
