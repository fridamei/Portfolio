data = "https://www.uio.no/studier/emner/matnat/math/STK1000/data/obligdata/oblig2/gene.txt"
genes <- read.table(data, header = TRUE)

attach(genes)

#Oppgave 1A
#Plott et histogram av genlengdene
hist(Gene.Lengths)
#Ser ikke ut til å være normalfordelt.
#Hovedtyngden er ikke i sentrum av utvalget, og kurven ligner ikke en bell-kurve.
#Forskjøvet mot venstre

#1B
#Gjennomsnitt:
mean(Gene.Lengths)
#Gjennomsnittslengden på genene i utvalget er 2610,39 nukleotider

#Standardavvik: 
sd(Gene.Lengths)
#Standardavviket er 1817,44

#1C
smpl <- sample(Gene.Lengths, 50)
mean(smpl)
#Gjennomsnittet i utvalget er 2607,42 nukleotider. Omtrent det samme som i det totale
#utvalget. Siden smpl er tilfeldig trukket av det større utvalget, bør gjennomsnittet her
#være det samme som i det totale utvalget.

#1D
#Utvalg med 50 genlengder (utvalget består altså av 50 tilfeldige observasjoner fra hele settet)
meanvec <- rep(0, 100)
for(i in 1:100){
  sample.now <- sample(Gene.Lengths, 50)
  meanvec[i] <- mean(sample.now)
}
hist(meanvec)

#Gjennomsnittet utvalgene ser ut til å være mer normalfordelt enn gjennomsnittet til det totale utvalget
#til fordelingen.
#Siden vi forventer at hver enkelt utvalg sitt gjennomsnitt vil ligge rundt det totale 
#gjennomsnittet, vil dermed tyngden av observasjonene ligge rundt nettopp dette gjennomsnittet.

#1E
#Dersom µ og sigma er sanne verdier av populasjonen, 
#skal μ¯x = µ og sigma¯x = sigma/n^0,5 = 1817,44/50^0,5 = 257,02. 
#Standardavvik = 257,02
#Gjennomsnitt = 2610,39

#Empirisk (faktisk utregnet):
sd(meanvec)
# = 220,08
mean(meanvec)
# = 2562,48
#Gjennomsnittet er nesten like. Standardavvikene devierer litt. Dersom man
#hadde hatt større utvalg (her var det 50 i hvert tilfeldige utvalg), ville man sannsynligvis
#fått verdier som samsvarte enda bedre, fordi når n øker, blir sigma¯x mindre

#1F

#Med n = 10:
#Teoretisk:
#μ¯x = µ og sigma¯x = sigma/n^0,5 = 1817,44/10^0,5 = 574,72. 
#Standardavvik = 574,72
#Gjennomsnitt = 2610,39

#Empirisk:
meanvec10 <- rep(0, 100)
for(i in 1:100){
  sample.now <- sample(Gene.Lengths, 10)
  meanvec10[i] <- mean(sample.now)
}


sd(meanvec10)
# = 538,31
mean(meanvec10)
# = 2590,62


#Med n = 100:
#Teoretisk:
#μ¯x = µ og sigma¯x = sigma/n^0,5 = 1817,44/100^0,5 = 181,7. 
#Standardavvik = 181,7
#Gjennomsnitt = 2610,39

#Empirisk:
meanvec100 <- rep(0, 100)
for(i in 1:100){
  sample.now <- sample(Gene.Lengths, 100)
  meanvec100[i] <- mean(sample.now)
}

sd(meanvec100)
# = 190,21
mean(meanvec100)
# = 2617,75

#1G
pnorm(3000, 2590.62, 538.31, lower.tail=FALSE)
# = 0,22
pnorm(3000, 2562.48, 220.08, lower.tail = FALSE)
# = 0,023
pnorm(3000, 2617.75, 190.21, lower.tail = FALSE)
# = 0,022

#1H
# Varians og bias:


