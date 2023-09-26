data = "http://www.uio.no/studier/emner/matnat/math/STK1000/data/vitruvisk.txt"
vitruvisk <- read.table(data,header=TRUE)

attach(vitruvisk)

#3A
summary(vitruvisk)
#Det ble gjennomført 150 undersøkelser på kvinner og 73 på menn
#Fempunktsoppummering kroppslengde: Min.: 152,0, Q1: 166,0, Median: 172,0, Q3: 178,0, Max.: 196,0
#Fempunktsoppsummering fot.navle: Min.: 87,0, Q1: 101,0, Median: 104,0, Q3: 109,0, Max.: 125,0

#3B
plot(vitruvisk$fot.navle,vitruvisk$kroppslengde,xlab="navlehyde",
     ylab="kroppslengde")

#Det ser ut som at kroppshøyden øker proporsjonalt med navlehøyden (ser ut som at målingene danner en forholdsvis lineær graf)

#3C
cor(kroppslengde, fot.navle)
#Korrelasjon sier noe om variablenes lineære relasjon.
#Dersom cor() = 1, er forholdet lineært.
#cor er i dette tilfellet 0.9140397,
#og det sannsynlig at man vil observere en større navle/fot-høyde
#hos personer med større kroppshøyde


#3D
fit <- lm(vitruvisk$kroppslengde~vitruvisk$fot.navle, data = vitruvisk)
plot(vitruvisk$fot.navle,vitruvisk$kroppslengde,xlab="navlehyde",
              ylab="kroppslengde")
linje<-abline(fit)

#3E
summary(fit)
#Ser på Coefficients, på andre rad:
#For hver cm navlehøyde, øker kroppshøyden med 1.27252

#3F
x<-vitruvisk$fot.navle
fit <- lm(vitruvisk$kroppslengde~x, data = vitruvisk)
plot(vitruvisk$fot.navle,vitruvisk$kroppslengde,xlab="navlehyde",
     ylab="kroppslengde")
linje<-abline(fit)
predict(fit, data.frame(x=c(121)))

#Usikker på hvorfor man må gi x-aksen et eget navn???
#Utfra regresjonen, vil en person med fot-navlehøyde være 192.8722 cm høy
#evt bruke y = 1,27252x+38,89675

#3G
summary(fit)
#Dersom man kvadrerer korrelasjonskoeffisienten, finner man 
#hvor mange prosent av variasjonene i høyde som er avhengig av variasjon i navlehøyde
#R^2 = 0.8355

#3H
plot(vitruvisk$fot.navle,residuals(fit))
abline(h=0)

#Uteliggere kan generelt anses som observasjoner som ligger utenfor 1,5*IQR, IQR er Q3-Q2
#IQR = 
#Dataene er tilsynelatende tilfeldig spredt om den horisontale aksen,
#og danner ingen tydelig mønster. Lineær regresjon vil derfor være en god modell

