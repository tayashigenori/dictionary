
# package を更新
list.of.packages <- c("arules")
new.packages <- list.of.packages[ !(list.of.packages %in% installed.packages()[,"Package"]) ]
if(length(new.packages)) install.packages(new.packages)

#
source("load_operands.R")

# tsv を読み込み
d = read.delim(
        "all.tsv",
        sep="\t",
        header=FALSE,
        colClasses=c( rep("factor", 26) ),
        na.strings = c("", "None")
        )
colnames(d) <- c(
    "CHAR",
    "HANZ-HEAD", "HANZ-SEMIVOWEL", "HANZ-NUCLEUS", "HANZ-LAST", "HANZ-TONE",
    "HONZ-HEAD", "HONZ-SEMIVOWEL", "HONZ-NUCLEUS", "HONZ-LAST", "HONZ-TONE",
    "HANJ-HEAD", "HANJ-SEMIVOWEL", "HANJ-NUCLEUS", "HANJ-LAST", "HANJ-TONE",
    "HANT-HEAD", "HANT-SEMIVOWEL", "HANT-NUCLEUS", "HANT-LAST", "HANT-TONE",
    "KANJ-HEAD", "KANJ-SEMIVOWEL", "KANJ-NUCLEUS", "KANJ-LAST", "KANJ-TONE"
)

# ルールを抽出
library(arules)
rules = apriori(
            d,
            parameter=list(support=0.001, confidence=0.8, maxlen=10),
# TODO
            appearance = list(
                lhs = c( kanj_all , honz_all ),
                default = "rhs"
            )
        )
print(rules)
rules.sorted <- sort(rules, by="support")
inspect( head(rules.sorted, n = 200) )

