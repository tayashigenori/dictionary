
# package を更新
list.of.packages <- c("arules")
new.packages <- list.of.packages[ !(list.of.packages %in% installed.packages()[,"Package"]) ]
if(length(new.packages)) install.packages(new.packages)

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
            parameter=list(support=0.001, confidence=0.8, maxlen=10),
            appearance = list(
                rhs = c(
                           "MAND-TONE=1", "MAND-TONE=2", "MAND-TONE=3", "MAND-TONE=4", "MAND-TONE=5",
                           "CANT-TONE=1", "CANT-TONE=2", "CANT-TONE=3", "CANT-TONE=4", "CANT-TONE=5", "CANT-TONE=6",
                           "CANT-TONE=7", "CANT-TONE=8", "CANT-TONE=9",
                           "VIET-TONE=1", "VIET-TONE=2", "VIET-TONE=3", "VIET-TONE=4", "VIET-TONE=5", "VIET-TONE=6",
                           "VIET-TONE=7", "VIET-TONE=8"
                       ),
                default = "lhs"
            )
        )
print(rules)
rules.sorted <- sort(rules, by="support")
inspect( head(rules.sorted, n = 200) )

