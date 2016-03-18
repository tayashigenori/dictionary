
cd ~/git/dictionary/rule_extractor/
for f in `find ../syllable_analyzer/feature_extractor/transaction2/ -type f`; do cat $f >> all.tsv ; done
Rscript assoc.R
rm all.tsv

