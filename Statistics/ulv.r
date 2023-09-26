'data ="http://www.uio.no/studier/emner/matnat/math/STK1000/data/wolves.txt"
wolf <- read.table(data,header=TRUE)

#2A:

#en kategorisk variabel er en variabel hvor individet plasseres i en gruppe eller en kategori. Ikke-numerisk data
#en kvantitativ variabel er en variabel som har en numerisk verdi, og som man kan utføre
#aritmetiske operasjoner på (og få et meningsfylt svar). Numerisk data
#kjønn og populasjon er kategoriske (enten tilhører man den ene eller den andre, måles ikke i tall)
#cpmg og tpmg er kvantitativ fordi det er en mengde som måles numerisk

#2B:

attach(wolf)
kjonn <- table(sex)
pie(kjonn)
#Det er undersøkt omtrent like mange hannulver som hunnulver

populasjon <- table(population)
pie(populasjon)
#De fleste av ulvene tilhørte den tungt jaktede populasjonen (nesten 3/4)

#2C: 

wolf.lett <- wolf[wolf[,"population"]==1,]
wolf.tungt <- wolf[wolf[,"population"]==2,]

#2D:

par(mfrow=c(2,2))
hist(wolf.lett$cpmg, main = "cpmg i lett jaktet")
boxplot(wolf.lett, main = "Lett jaktet")
hist(wolf.tungt$cpmg, main ="cpmg i tungt jaktet")
boxplot(wolf.tungt, main = "Tungt jaktet")

#For cpmg-histogramene: i den tungt jaktede populasjonen ligger
#observasjonene generelt på høyere nivåer enn hos den lett jaktede. 
#Hovedtyngden ligger i midlertid mellom 10 og 15 for begge populasjoner.
#Boksplot: populasjon har bare én tett strek i hhv. 1 og 2 fordi dette er kategorisk data 
#Første kvartil ligger lavere i lett jaktet (boksens nedre avgrensning)
#og verdimengden (øverste horisontale strek) er også litt lavere. Dessuten er tredje kvartil lavere.
#Boksen representerer 50 % av observasjonene, vi ser derfor at 50 % av observasjonene er forskjøvet
#litt opp i tungt jaktet sammenlignet med lett jaktet. 
#Boksene er omtrent like store (altså har begge populasjoner omtrent like stor spredning)

#2E
mean(wolf.lett$cpmg)
# 15,56
median(wolf.lett$cpmg)
#14,24
mean(wolf.tungt$cpmg)
#17,07
median(wolf.tungt$cpmg)
#16,32

#Gjennomsnittet og medianen ligger begge høyere for tungt jaktet.
#Siden gjennomsnittet er høyere enn medianen for begge populasjoner,
#er fordelingen forskjøvet mot høyre (altså at det er flere observasjoner
#som er større enn medianen enn mindre)
#Siden gjennomsnittet ikke er likt medianen, er heller ikke utvalgene
#helt normalfordelt

#2F: 
#Standardavvik og gjennomsnitt passer godt for studier hvor
#observasjonene er symmetriske og uten sterke uteliggere (fordi gjennomsnittet er sensitivt for ekstreme verdier)
#Fempunktsoppsummering passer godt hvor observasjonene er mer spredt.
#Basert på histogrammene, er lett jaktet nok best egnet for fempunktsoppsummering
#fordi den har en del observasjoner i ytre del av verdimengden som vil trekke opp gjennomsnittet
#Tung jaktet er mer symmetrisk og ville passet bedre for fempunktsoppsummering, men også denne har noen ekstreme uteliggere
#i øvre sjikte av verdimengden.

#2G
qqnorm(wolf.lett$cpmg)
qqline(wolf.lett$cpmg)
#Ser at en særlig observasjonene i øvre del av verdimengden ikke sammenfaller
#med linjen på QQ-plotet. Det virker ikke som den er normalfordelt

qqnorm(wolf.tungt$cpmg)
qqline(wolf.tungt$cpmg)
#Her er punktene stort sett på linjen, og den er tilnærmet normalfordelt

