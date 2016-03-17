
mand_all <- scan("mandarin/sorted.uniq.txt", what="", sep="\n")
mand_hd  <- scan("mandarin/head.txt",        what="", sep="\n")
mand_sv  <- scan("mandarin/semi_vowel.txt",  what="", sep="\n")
mand_nc  <- scan("mandarin/nucleus.txt",     what="", sep="\n")
mand_lt  <- scan("mandarin/last.txt",        what="", sep="\n")
mand_tn  <- scan("mandarin/tone.txt",        what="", sep="\n")

cant_all <- scan("cantonese/sorted.uniq.txt", what="", sep="\n")
cant_hd  <- scan("cantonese/head.txt",        what="", sep="\n")
cant_sv  <- scan("cantonese/semi_vowel.txt",  what="", sep="\n")
cant_nc  <- scan("cantonese/nucleus.txt",     what="", sep="\n")
cant_lt  <- scan("cantonese/last.txt",        what="", sep="\n")
cant_tn  <- scan("cantonese/tone.txt",        what="", sep="\n")

kore_all <- scan("korean/sorted.uniq.txt", what="", sep="\n")
kore_hd  <- scan("korean/head.txt",        what="", sep="\n")
kore_sv  <- scan("korean/semi_vowel.txt",  what="", sep="\n")
kore_nc  <- scan("korean/nucleus.txt",     what="", sep="\n")
kore_lt  <- scan("korean/last.txt",        what="", sep="\n")
kore_tn  <- scan("korean/tone.txt",        what="", sep="\n")

viet_all <- scan("vietnamese/sorted.uniq.txt", what="", sep="\n")
viet_hd  <- scan("vietnamese/head.txt",        what="", sep="\n")
viet_sv  <- scan("vietnamese/semi_vowel.txt",  what="", sep="\n")
viet_nc  <- scan("vietnamese/nucleus.txt",     what="", sep="\n")
viet_lt  <- scan("vietnamese/last.txt",        what="", sep="\n")
viet_tn  <- scan("vietnamese/tone.txt",        what="", sep="\n")

japa_all <- scan("japanese/sorted.uniq.txt", what="", sep="\n")
japa_hd  <- scan("japanese/head.txt",        what="", sep="\n")
japa_sv  <- scan("japanese/semi_vowel.txt",  what="", sep="\n")
japa_nc  <- scan("japanese/nucleus.txt",     what="", sep="\n")
japa_lt  <- scan("japanese/last.txt",        what="", sep="\n")
japa_tn  <- scan("japanese/tone.txt",        what="", sep="\n")


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
#            appearance = list(
#                rhs=mand_tn,
#                default="lhs"
#            )
        )
print(rules)
rules.sorted <- sort(rules, by="support")
inspect( head(rules.sorted, n = 200) )

