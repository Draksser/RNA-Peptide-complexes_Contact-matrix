#! /bin/bash


cp dist_NX_PY.xvg dist_NX_PY_exp.xvg
sed -i -e '/#/d' -e '/@/d' dist_NX_PY_exp.xvg
sed -i 's/  /!/g' dist_NX_PY_exp.xvg
cat dist_NX_PY_exp.xvg | cut -d '!' -f 2 > final_NX_PY.xvg
rm dist_NX_PY_exp.xvg
cp final_NX_PY.xvg final_NX_PY.txt
rm final_NX_PY.xvg
exit 0


