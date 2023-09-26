data = "http://www.uio.no/studier/emner/matnat/math/STK1000/data/zebrafinch.txt"
zebrafinch <- read.table(data,header=TRUE)

attach(zebrafinch)

#1A
hist(zebrafinch$BMR)
#BMR er symmetrisk fordelt om 0,8-0,9, hvor hovedtyngden av observasjonene ligger
#Ligner en bell-kurve.Kan ikke se noen uteliggere.

#1B
mean(BMR)
# = 0.8485003
#Gjennomsnittet av alle observasjonene, sensitiv for ekstreme uteliggere.
median(BMR)
# = 0.8397846
#Den midterste observasjonen. Påvirkes lite av uteliggere

#1C
sd(BMR)
# = 0.1134001
#Beskriver spredningen til observasjonene fra gjennomsnittet
#Lavt standardavvik vil si at observasjonene ligger nær gjennomsnittet
IQR(BMR)
# = 0.1517731
#Q3 - Q1, er verdiområdet hvor 50 % av de midterste observasjonene ligger.
#Kan blant annet brukes til å identifisere uteliggere.

#1D
qqnorm(BMR)
qqline(BMR)
#Punktene devierer svært lite fra linjen
#Kan dermed si med stor sikkerhet at BMR er normalfordelt

#1E

#standardisert verdi av BMR: z = (X-my)/sigma = (X-gj.snitt)/s,
#der X er observasjonen vi vil sjekke z-verdien for. Sigma er standardavvik,
#og my er gjennomsnittet.
z <- (0.8-mean(BMR))/sd(BMR)
print(z)
# z = -0,4276918
#z-scoren indikerer hvor mange standardavvik observasjonen er unna gjennomsnittet

#1F
#pnorm() gir sannsynligheten for at observasjoner ligger mellom minus uendelig og grensen man angir 
#(altså sannsynligheten for at observasjoner ligger til venstre på kurven for grensen man vil undersøke)
#pnorm(x, gj.snitt, standardavvik)
pnorm(0.8)
# = 0.7881446, altså 78,8 % sannsynlighet for at en observasjon er <0,8

#1G
#for å finne sannsynligheten for at noe er større enn den gitte grensa: 
#1- pnorm(x, gj.snitt, standardavvik)

1-pnorm(1)
# = 0.1586553, 15,9 % sannsynlighet for at en fink har BMR > 1