library(MASS)
cats

#OPPGAVE 3A
bwt <- cats$Bwt
hwt <- cats$Hwt

plot(bwt, hwt, xlim = c(1.6, 4), ylim = c(3, 22),
     xlab = "Kroppsvekt", ylab = "Hjertevekt", main = "Forhold hjertevekt/kroppsvekt hos katter")


#Det ser ut som det til en viss grad er en lineær sammenheng
#mellom kroppsvekt og hjertevekt hos katter
#Den generelle tendensen er at hjertevekten øker med kroppsvekten

#3B
fit <- lm(cats$Hwt~cats$Bwt, data = cats)
linje <- abline(fit)


#3C
#Antagelser:
# 1. At det faktisk er et lineært forhold mellom variablene
# 2. At residualene (avstanden mellom punktene og regresjonslinja) er normalfordelt, sjekkes med et qq plot
# 3. At de uavhengige dataene ikke har for sterk korrelasjon
# 4. At det ikke er autokorrelasjon i dataene (at de forskjellige målingene ikke er uavhengig av hverandre, 
# altså når y(x+1) ikke er uavhengig av y(x))
# 5. At punktene er jevnt fordelt om regresjonslinja for alle x-verdier (at ikke spredningen øker når x øker feks)

#1 stemmer basert på boxplotet
#2 normalfordelt hvis punktene ligger på en qq-linje, og det gjør de
#3 bare en uavhengig data (kroppsvekt)
#4 det er forskjellige katter, så en katts størrelse og hjertevekt
# er uavhengig av de andres
#5 ser fra plot(bwt, res) at punktene er jevnt spredt om linja for alle x


res <- residuals(fit)
plot(bwt, res)
abline(h=0)
qqnorm(res)
qqline(res)

#3D

summary(fit)
#For hver kg kroppsvekt, øker hjertevekten med 4,03 gram

#3E
#Null-hypotesen er at det er ikke er en sammenheng 
#mellom kroppvekt og hjertevekt. Siden p-verdien er veldig lav, 
#er det veldig lav sannsynlighet for at null-hypotesen stemmer, 
#altså er det sannsynlig at det er en sammenheng

#3F
b1 <- summary(fit)$coefficients[2, 1]
se.b1 <- summary(fit)$coefficients[2, 2]
df <- fit$df.residual
lower <- b1 + qt(0.025, df) * se.b1
upper <- b1 + qt(0.975, df) * se.b1


#??????

#3G
plot(bwt, hwt, xlim = c(1.6, 4), ylim = c(3, 22),
     xlab = "navn x-akse", ylab = "navn y-akse", main = "tittel")
abline(fit)
xval <- seq(1, 4.5, by = 0.01)
new <- data.frame(bwt = xval)
pred.int <- predict(fit, newdata = new, interval = "prediction")
mean.int <- predict(fit, newdata = new, interval = "confidence")
matlines(xval, cbind(pred.int[, 2], pred.int[, 3]), lty =
           2, col = "steelblue")
matlines(xval, cbind(mean.int[, 2], mean.int[, 3]), lty =
           2, col = "tomato")

#??
