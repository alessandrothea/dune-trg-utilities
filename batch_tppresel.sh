# ./trgtree_slimmer.py -m pgun ./data/eminus/data-fixed/*.root  -o data/eminus/tp_presel
# ./trgtree_slimmer.py -m pgun ./data/gammas/data-fixed/*.root  -o data/gammas/tp_presel
# ./trgtree_slimmer.py -m pgun ./data/muminus/data-fixed/*.root  -o data/muminus/tp_presel
# ./trgtree_slimmer.py -m bkg ./data/radbkg/data-fixed/*.root  -o data/radbkg/tp_presel

# ./rmerger.py -o ./data/eminus/vd_1x8x6_eminus_center_2333289_tppresel_ana.ntuple.root  ./data/eminus/tp_presel/*.root
# ./rmerger.py -o ./data/gammas/vd_1x8x6_gamma_center_2333392_tppresel_ana.ntuple.root ./data/gammas/tp_presel/*.root
# ./rmerger.py -o ./data/muminus/vd_1x8x6_muminus_center_2333393_tppresel_ana.ntuple.root data/muminus/tp_presel/*.root 
./rmerger.py -o ./data/radbkg/vd_1x8x6_radbkg_2333394_23335306_233378794_tppresel_ana.ntuple.root ./data/radbkg/tp_presel/*.root
# ./rmerger.py -o ./data/radbkg/vd_1x8x6_radbkg_tppresel_ana.XXX.ntuple.root ./data/radbkg/tp_presel/*2337894_*{0,1,2,3,4,5,6,7,8,9}_*.root
# ./rmerger.py -o ./data/radbkg/vd_1x8x6_radbkg_tppresel_ana.XXX.ntuple.root ./data/radbkg/tp_presel/*2337894_*.root
# ./rmerger.py -o ./data/radbkg/vd_1x8x6_radbkg_tppresel_ana.XXX.ntuple.root ./data/radbkg/tp_presel/*.root
# ./rmerger.py -o ./data/radbkg/vd_1x8x6_radbkg_tppresel_ana.YYY.ntuple.root ./data/radbkg/tp_presel/*.root