data = "https://www.uio.no/studier/emner/matnat/math/STK1000/data/obligdata/oblig2/vitruvisk75.txt"
vitruvisk <- read.table(data, header = TRUE)

attach(vitruvisk)
davinci <- vitruvisk$kroppslengde / vitruvisk$fot.navle

#Oppgave 2A

summary(davinci)
hist(davinci)
sd(davinci)
#Standardavvik er 0,038
#Medianen er 1,642
#Gjennomsnittet 1,645
#Den minste observasjonen er 1,482
#Første kvartil deler de laveste 25 % av dataene med de øvre 75 % = 1,622
#Medianen er 1,642
#Tredje kvartil deler øvre 25 % og nedre 75 % = 1,667
#Maksverdien er 1,851
#Ser ut som at histogrammet kan minne om formen til en Bell-kurve,
#dette ville nok kommet bedre frem om man hadde hatt flere verdier på x-aksen. 

qqline(Gene.Lengths)
qqnorm(Gene.Lengths)
#Dersom utvalget hadde vært normalfordelt, ville observasjonene lagt langs den 
#rette linja. Kan ikke anta normalfordeling utfra dette plottet

#2B
#Bruker t-test fordi vi ikke kjenner det sanne standardavviket ???
#Antagelser som ligger til grunn:

#2C
#Det gylne snitt: 1,618
#Null-hypotese: kroppslengde og fot.navle følger det gylne snitt;
# det gylne snitt = 1,618, gjennomsnitt i utvalget = 1,645
#Alternativ hypotese: de følger ikke det gylne snitt
#To-sidig hypotese 2*P(Z>=X), der Z = estimat - hypotese/standardavvik til estimatet (sigma/n^0,5)
# (1,645-1,618)/(0,038/75^0,5) = 

t.test(davinci, y= NULL, "two.sided", mu=1.618)
#p = 0,0000001225
#Sannsynligheten for at de to er like gitt utvalget er altså lik p,
#siden p er under 0,05 (gitt at vi operer med 95 % konf.intervaller) forkaster vi null-hypotesen
#og konkluderer med at forholdet mellom kroppslengde og fot.navle ikke følger det gyldne snitt


#2D
#I et 90 prosent konfidensintervall er det 90 prosent sannsynlighet for at den
#sanne verdien (den som stemmer for hele populasjonen) ligger innenfor
#Dette vil være smalere enn både 95 % og 99 % konfidensintervallene 
#(fordi dersom intervallet er lite, er det litt mindre sannsynlig at verdien er innenfor)

t.test(davinci, y= NULL, "two.sided", mu=1.618, conf.level = 0.90)
#konf.intervall: [1,636, 1,651]
t.test(davinci, y= NULL, "two.sided", mu=1.618, conf.level = 0.95)
#konf.int: [1,635, 1,652]
t.test(davinci, y= NULL, "two.sided", mu=1.618, conf.level = 0.99)
#konf.int: [1,632, 1,655]

#Ingen av konfidensintervallene inneholder 1,618, så vi kan ikke konkludere
#med at forholdet følger det gylne snitt for noen av intervallene

#2E
davinci.hoy <- davinci[vitruvisk$kroppslengde >= 175]
davinci.lav <- davinci[vitruvisk$kroppslengde < 175]

#Null-hypotese: det er ikke forskjell i forholdet mellom kroppslengde og 
#fot.navle hos høye og lave

t.test(davinci.hoy, davinci.lav)
# p = 0,44
# Det er altså 44 % sannsynlighet for at vi faktisk får at forholdet i de to gruppene
# er like, altså for at vi observerer null-hypotesen gitt de to utvalgene.
# Vi kan dermed ikke forkaste null-hypotesen, og det er sannsynlig at forholdet faktisk er likt
