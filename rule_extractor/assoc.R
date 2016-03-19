
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
    "MAND-HEAD", "MAND-SEMIVOWEL", "MAND-NUCLEUS", "MAND-LAST", "MAND-TONE",
    "CANT-HEAD", "CANT-SEMIVOWEL", "CANT-NUCLEUS", "CANT-LAST", "CANT-TONE",
    "KORE-HEAD", "KORE-SEMIVOWEL", "KORE-NUCLEUS", "KORE-LAST", "KORE-TONE",
    "VIET-HEAD", "VIET-SEMIVOWEL", "VIET-NUCLEUS", "VIET-LAST", "VIET-TONE",
    "JAPA-HEAD", "JAPA-SEMIVOWEL", "JAPA-NUCLEUS", "JAPA-LAST", "JAPA-TONE"
)

# ルールを抽出
library(arules)
rules = apriori(
            d,
            parameter=list(support=0.001, confidence=0.8, maxlen=10)
# TODO
#            appearance = list(
#                rhs = c(mand_tns, cant_tns, viet_tns)
#                default = "lhs"
#            )
        )
print(rules)
rules.sorted <- sort(rules, by="support")
inspect( head(rules.sorted, n = 200) )

