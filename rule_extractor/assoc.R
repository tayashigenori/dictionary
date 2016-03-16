
list.of.packages <- c("arules")
new.packages <- list.of.packages[ !(list.of.packages %in% installed.packages()[,"Package"]) ]
if(length(new.packages)) install.packages(new.packages)

library(arules)
d = read.csv(
        "all.csv",
        header=FALSE,
        na.strings = c("",
                       "[Mand:hd]", "[Mand:sv]", "[Mand:lt]",
                       "[Cant:hd]", "[Cant:sv]", "[Cant:lt]",
                       "[Viet:hd]", "[Viet:sv]", "[Viet:lt]",
                       "[Kore:hd]", "[Kore:sv]", "[Kore:lt]", "[Kore:tn]None",
                       "[Japa:hd]", "[Japa:sv]", "[Japa:lt]", "[Japa:tn]None"
                      )
        )
rules = apriori(
            d,
            parameter=list(support=0.001, confidence=0.8, maxlen=10)
        )
print(rules)
rules.sorted <- sort(rules, by="support")
inspect( head(rules.sorted, n = 200) )

