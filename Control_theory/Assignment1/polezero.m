T_M = 2
T_D = 1
K = linspace(-8, 8, 20)
H = tf([0 T_D*K K], [T_M 1+T_D*K K])

pzplot(H)
grid