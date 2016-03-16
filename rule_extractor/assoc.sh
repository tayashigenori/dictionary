
cd ~/git/dictionary/rule_extractor/
for f in `find ../syllable_analyzer/feature_extractor/transaction/ -type f`; do cat $f >> all.csv ; done
Rscript assoc.R
rm all.csv

