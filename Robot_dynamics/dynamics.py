# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 02:26:44 2021

@author: frida
"""

# from pprint import pprint
import sympy as sp
import numpy as np
import sympy.physics.vector as spv
from sympy.physics.vector import dynamicsymbols

"Søk etter disse variablene i koden for å skru av og på printing av de forskjellige tinga"
print_v_w = ""
print_A_matriser = ""
print_kinematics = ""



def A_matrix(DH_array):
    # rot_z, trans_z, trans_a, rot_a
    row_1 = sp.Array([sp.cos(DH_array[0]), -sp.sin(DH_array[0])*sp.cos(DH_array[3]), sp.sin(DH_array[0])*sp.sin(DH_array[3]), DH_array[2]*sp.cos(DH_array[0])])
    row_2 = sp.Array([sp.sin(DH_array[0]), sp.cos(DH_array[0])*sp.cos(DH_array[3]), -sp.cos(DH_array[0])*sp.sin(DH_array[3]), DH_array[2]*sp.sin(DH_array[0])])
    row_3 = sp.Array([0, sp.sin(DH_array[3]), sp.cos(DH_array[3]), DH_array[1]])
    row_4 = sp.Array([0, 0, 0, 1])

    A_i = sp.Matrix([row_1,
           row_2,
           row_3,
           row_4])

    return A_i

def jacobian_2dof(A1, A2, rot_liste): # rot_liste er den boolske lista som indikerer om leddene er rotasjons- eller translasjonsledd
    R0 = sp.Matrix([[1,0,0], [0,1,0], [0,0,1]]) # Brukes for ledd 1
    # A1 brukes for ledd 2    
    A2_0 = A1 @ A2 # Brukes  for å finne o_n
    
    "Posisjonsvektorer, hentet fra fjerde kolonne i transformasjonsmatrisene"
    o_n = sp.Matrix(A2_0[:3, 3]) 
    o_1 = sp.Matrix(A1[:3, 3])
    # o_0 = [0,0,0], men trenger ikke bruke den fordi man skal subtrahere den og den er 0

    "Ledd 1"
    z0 = sp.Matrix(R0[:3, 2])
    on_0 = sp.Matrix(o_n) # O_n - O_0, der o_0 er [0,0,0]
    
    # Hvis ledd 1 er et rotasjonsledd: 
    if rot_liste[0]:
        Jv1 = z0.cross(on_0)
        #Jv1 = np.cross(z0, on_0, axis=0)
        Jw1 = z0
    # Hvis det er et translasjonsledd:
    else:
        Jv1 = z0
        Jw1 = sp.Matrix([0,0,0])
    
    "Ledd 2"
    z1 = sp.Matrix(A1[:3, 2])
    on_1 = sp.Matrix(o_n - o_1)
    # Hvis ledd 2 er et rotasjonsledd:
    if rot_liste[1]:
        Jv2 = z1.cross(on_1)
        Jw2 = z1
    else:
        Jv2 = z1
        Jw2 = sp.Matrix([0,0,0])

    "Setter sammen til en Jacobi-matrise"
    Jv = sp.simplify(sp.Matrix([[Jv1, Jv2]]))        
    Jw = sp.simplify(sp.Matrix([[Jw1, Jw2]]))
    
    Jv = (sp.Matrix([[Jv1, Jv2]]))        
    Jw = (sp.Matrix([[Jw1, Jw2]]))
    jacobian = sp.Matrix([Jv, Jw])
    return jacobian

def jacobian_3dof(A1, A2, A3, rot_liste): # rot_liste er den boolske lista som indikerer om leddene er rotasjons- eller translasjonsledd
    R0 = sp.Matrix([[1,0,0], [0,1,0], [0,0,1]]) # Brukes for ledd 1
    # A1 brukes for ledd 2    
    A2_0 = A1 @ A2 # Brukes for ledd 3
    A3_0 = A2_0 @ A3 # Brukes kun til å finne o_n
    
    "Posisjonsvektorer, origo"
    o_n = sp.Matrix(A3_0[:3, 3]) # Posisjonen til endeeffektoren, 3 x 1 vektor i homogen transformasjonsmatrise
    o_2 = sp.Matrix(A2_0[:3, 3]) 
    o_1 = sp.Matrix(A1[:3, 3])
    # o_0 = [0,0,0], men trenger ikke bruke den fordi man skal subtrahere den og den er 0

    "Ledd 1"
    z0 = sp.Matrix(R0[:3, 2])
    on_0 = sp.Matrix(o_n) # O_n - O_0, der o_0 er [0,0,0]
    # Hvis ledd 1 er et rotasjonsledd: 
    if rot_liste[0]:
        Jv1 = z0.cross(on_0)
        Jw1 = z0
    # Hvis det er et translasjonsledd:
    else:
        Jv1 = z0
        Jw1 = sp.Matrix([0,0,0])
    
    "Ledd 2"
    z1 = sp.Matrix(A1[:3, 2])
    on_1 = sp.Matrix(o_n - o_1)
    # Hvis ledd 2 er et rotasjonsledd:
    if rot_liste[1]:
        Jv2 = z1.cross(on_1)
        Jw2 = z1
    else:
        Jv2 = z1
        Jw2 = sp.Matrix([0,0,0])
    
    "Ledd 3"
    z2 = sp.Matrix(A2_0[:3, 2])
    on_2 = sp.Matrix(o_n - o_2)
    # Hvis rotasjonsledd
    if rot_liste[2]:
        Jv3 = z2.cross(on_2)
        Jw3 = z2
    # Hvis translasjonsledd
    else:
        Jv3 = z2
        Jw3 = sp.Matrix[0,0,0]    
        
    "Lager Jacobi-matrisen"
    Jv = sp.simplify(sp.Matrix([[Jv1, Jv2, Jv3]]))           
    Jw = sp.simplify(sp.Matrix([[Jw1, Jw2, Jw3]]))
    
    "Uten simplify, for å vise utregning"
    Jv = (sp.Matrix([[Jv1, Jv2, Jv3]]))     
    Jw = (sp.Matrix([[Jw1, Jw2, Jw3]]))
    
    jacobian = sp.Matrix([Jv, Jw])
    
    return jacobian

def jacobian_4dof(A1, A2, A3, A4, rot_liste): # rot_liste er den boolske lista som indikerer om leddene er rotasjons- eller translasjonsledd
    R0 = sp.Matrix([[1,0,0], [0,1,0], [0,0,1]]) # Brukes for ledd 1
    # A1 brukes for ledd 2    
    A2_0 = A1 @ A2 # Brukes for ledd 3
    A3_0 = A2_0 @ A3 # brukes for ledd 4
    A4_0 = A3_0 @ A4 # Brukes kun til å finne o_n
    
    o_n = sp.Matrix(A4_0[:3, 3]) # Fjerde kolonne, 3 x 1 vektor i homogen transformasjonsmatrise
    o_3 = sp.Matrix(A3_0[:3, 3]) 
    o_2 = sp.Matrix(A2_0[:3, 3]) 
    o_1 = sp.Matrix(A1[:3, 3])
    
    "Ledd 1"
    z0 = sp.Matrix(R0[:3, 2])
    on_0 = sp.Matrix(o_n) # O_n - O_0
    # Hvis ledd 1 er et rotasjonsledd: 
    if rot_liste[0]:
        Jv1 = z0.cross(on_0)
        Jw1 = z0
    # Hvis det er et translasjonsledd:
    else:
        Jv1 = z0
        Jw1 = sp.Matrix([0,0,0])
    
    "Ledd 2"
    z1 = sp.Matrix(A1[:3, 2])
    on_1 = sp.Matrix(o_n - o_1)
    # Hvis ledd 2 er et rotasjonsledd:
    if rot_liste[1]:
        Jv2 = z1.cross(on_1)
        Jw2 = z1
    else:
        Jv2 = z1
        Jw2 = sp.Matrix([0,0,0])
 
    "Ledd 3"
    z2 = sp.Matrix(A2_0[:3, 2])
    on_2 = sp.Matrix(o_n - o_2)
    # Hvis rotasjonsledd
    if rot_liste[2]:
        Jv3 = z2.cross(on_2)
        Jw3 = z2
    # Hvis translasjonsledd
    else:
        Jv3 = z2
        Jw3 = sp.Matrix[0,0,0] 
    
    "Ledd 4"
    z3 = sp.Matrix(A3_0[:3, 2])
    on_3 = sp.Matrix(o_n - o_3)
    # Hvis rotasjonsledd
    if rot_liste[3]:
        Jv4 = z3.cross(on_3)
        Jw4 = z3
    # Hvis translasjonsledd
    else:
        Jv4 = z3
        Jw4 = sp.Matrix([0,0,0])

    "Setter sammen til Jacobi-matrise"
    Jv = sp.simplify(sp.Matrix([[Jv1, Jv2, Jv3, Jv4]]))        
    Jw = sp.simplify(sp.Matrix([[Jw1, Jw2, Jw3, Jw4]]))
    
    Jv = (sp.Matrix([[Jv1, Jv2, Jv3, Jv4]]))        
    Jw = (sp.Matrix([[Jw1, Jw2, Jw3, Jw4]]))
    jacobian = sp.Matrix([Jv, Jw])
    
    return jacobian_matrix

# For å finne singulariteter:
def determinant_jacobian(J):
    detJ = sp.solve(J.det())
    return detJ

def torque(lagrangian, q_liste, q_dot_liste):
    "Ledd 1"
    # dL/d(q_dot_1), Lagrangian derivert mhp hastighet ledd 1
    dL_dqdot1 = sp.diff(lagrangian, q_dot_liste[0])
    
    # d(dL/dqdot1)dt, den over derivert mhp tiden
    L1_dt = sp.diff(dL_dqdot1, sp.symbols('t'))
    
    # dL/dq1, Lagrangian derivert mhp q1
    L_dq1 = sp.diff(lagrangian, q_liste[0])
    
    torque1 = sp.simplify(L1_dt - L_dq1)
    
    "Ledd 2"
    # dL/d(q_dot_2), Lagrangian derivert mhp hastighet ledd 2
    dL_dqdot2 = sp.diff(lagrangian, q_dot_liste[1])
    
    # d(dL/dqdot1)dt, den over derivert mhp tiden
    L2_dt = sp.diff(dL_dqdot2, sp.symbols('t'))
    
    # dL/dq1, Lagrangian derivert mhp q1
    L_dq2 = sp.diff(lagrangian, q_liste[1])
    
    torque2 = sp.simplify(L2_dt - L_dq2)
    
    return torque1, torque2


def main(_):
    # KOPIER FRA A-MATRISE-FILA DERSOM MAN HAR BRUKT DEN FØRST, SÅ SLIPPER MAN Å SKRIVE DOBBELT OPP
    
    "Generiske variabler"
        # Rotasjonsledd
    q1, q2, q3, q4 = (sp.symbols('theta_1 theta_2 theta_3 theta_4'))
        # Prismatiske ledd
    d1, d2, d3 = sp.symbols('d1 d2 d3')
        # Linklengder
    L1, L2, L3, L4 = sp.symbols('L1 L2 L3 L4')
    Loff = sp.symbols('L_off')
        # Vinkler 
    pi = sp.pi
    nitti = sp.pi/2   
    
    
    "DH-tabell"
        # rot_z, trans_z, trans_x, rot_x
        # theta, d, a, alfa
    ledd1 = sp.Array([q1, L1, Loff, -nitti])
    ledd2 = sp.Array([0, L2+d2, 0, 0])
    ledd3 = sp.Array([0, 0, 0, 0])

    ledd4 = sp.Array([q4, L3+L4, 0, 0])
    
    "A-matriser"
    A1 = A_matrix(ledd1)
    A2 = A_matrix(ledd2)
    A3 = A_matrix(ledd3)
    A4 = A_matrix(ledd4)



    "Endre denne dersom ingen print"
    print_A_matriser = False
    
    
    if print_A_matriser:
        print("\nA\N{SUBSCRIPT ONE}:\n")
        sp.pprint(A1)
        
        print("\n\nA\N{SUBSCRIPT TWO}:\n")
        sp.pprint(A2)
        
        print("\n\nA\N{SUBSCRIPT THREE}:\n")
        sp.pprint(A3)
        
        print("\n\nA\N{SUBSCRIPT TWO}\N{SUPERSCRIPT ZERO} = A\N{SUBSCRIPT ONE} * A\N{SUBSCRIPT TWO}:\n")
        sp.pprint(A1@A2)

        # Dersom A3_0 ikke er den homogene transformasjonen (det er en A4 også) 
        #print("\n\nA\N{SUBSCRIPT THREE}\N{SUPERSCRIPT ZERO} = A\N{SUBSCRIPT ONE} * A\N{SUBSCRIPT TWO} * A\N{SUBSCRIPT THREE}:\n")
        
        
        print("\nHomogen transformasjonsmatrise:" 
              "T\N{SUBSCRIPT THREE}\N{SUPERSCRIPT ZERO} = "
              "A\N{SUBSCRIPT THREE}\N{SUPERSCRIPT ZERO} = A\N{SUBSCRIPT ONE} * " 
              "A\N{SUBSCRIPT TWO} * A\N{SUBSCRIPT THREE}:\n")
        sp.pprint(A1@A2@A3)
        
 
    "Kjøring Jacobian"
   
    "FYLL INN"
    N_DOF = 2 # Antall DOF, sett inn 2, 3 eller 4    
    
    if N_DOF == 2:
        "FYLL INN"
        joint_types = [True, False] # hva slags ledd manipulatoren har, True for rotasjon, False for translatorisk 
        jacobian = jacobian_2dof(A1, A2, joint_types)
        jacobian_simpl = sp.simplify(jacobian)

    
    elif N_DOF == 3:
        "FYLL INN"
        joint_types = [False, False, False] # hva slags ledd manipulatoren har, True for rotasjon, False for translatorisk 
        jacobian = jacobian_3dof(A1, A2, A3, joint_types)
        jacobian_simpl = sp.simplify(jacobian)
        
    elif N_DOF == 4:
        
        joint_types = [False, False, False, False] # hva slags ledd manipulatoren har, True for rotasjon, False for translatorisk 
        jacobian = jacobian_4dof(A1, A2, A3, A4, joint_types)
        jacobian_simpl = sp.simplify(jacobian)
    
    
    """
    
    Kinematikk, 2DOF:
        Først gjort Jacobimatrisen uavhengig for de enkelte leddene
        (alt tilknyttet ledd 2 = 0 for ledd 1, dvs hele andre kolonne samt alle L2 i første kolonne)
        Deretter ganget med en vektor med leddhastighetene, q_dot
        
        Bare å fylle på dersom vi får manipulator med flere ledd   
        

    """

    q_dot1, q_dot2, q_dot3 = dynamicsymbols('theta_1 theta_2 theta_3', 1)
    # Dersom det er prismatiske ledd også
    d_dot1, d_dot2, d_dot3 = dynamicsymbols('d1 d2 d3', 1)


    
    "FYLL INN"
    "Endre denne lista etter hva slags ledd manipulatoren har!"
    q_dot = sp.Matrix([q_dot1, d_dot2])
    
    
    
    
    "Bytt ut variablene som tilhører ledd 2 med 0, slik at man får ledd 1 uavhengig av ledd 2"
        # Setter først hele kolonna til ledd 2 lik 0
    zero = sp.zeros(6, 1)
    
    J1 = sp.Matrix([[jacobian_simpl[:, 0], zero]])
    J1 = J1.subs(L2, 0)
    J1 = J1.subs(d2, 0)
    Jv1 = J1[:3, :]
    Jw1 = J1[3:, :]
    
    Jv2 = jacobian_simpl[:3, :]    
    Jw2 = jacobian_simpl[3:, :]
    
    v1 = Jv1 * q_dot
    w1 = Jw1 * q_dot
    v2 = Jv2 * q_dot
    w2 = Jw2 * q_dot
 
    """
    Hvis det er tre ledd: 
        J1 = sp.Matrix([[jacobian_simpl[:, 0], zero, zero]])
        J1 = J1.subs(L2, 0)
        J1 = J1.subs(L3, 0)
        Jv1 = J1[:3, :]
        Jw1 = J1[3:, :]
        
        J2 = sp.Matrix([[jacobian_simpl[:, :2], zero]])
        J2 = J2.subs(L3, 0)
        Jv2 = J2[:3, :]
        Jw2 = J2[3:, :]
        
        Jv3 = jacobian_simpl[:3, :]    
        Jw3 = jacobian_simpl[3:, :]
        
        v1 = Jv1 * q_dot
        w1 = Jw1 * q_dot
        v2 = Jv2 * q_dot
        w2 = Jw2 * q_dot
        v3 = Jv3 * q_dot
        w3 = Jw3 * q_dot
    """
   
    "FYLL INN"
    "Dersom man ønsker utskrift"
    print_v_w = False

    
    if print_v_w:
        print("\nV\N{SUBSCRIPT ONE}:\n")
        sp.pprint(v1)
        print("\n\n\N{GREEK SMALL LETTER OMEGA}\N{SUBSCRIPT ONE}:\n")
        sp.pprint(w1)

        print("\nV\N{SUBSCRIPT TWO}:\n")
        sp.pprint(v2)
        print("\n\n\N{GREEK SMALL LETTER OMEGA}\N{SUBSCRIPT TWO}:\n")
        sp.pprint(w2) 
       


    "Selve kinematikken:"
    m1, m2, m3, g = sp.symbols('m1 m2 m3 g')
    
    I1x, I1y, I1z, I2x, I2y, I2z, I3x, I3y, I3z = sp.symbols('I1x I1y I1z I2x I2y I2z I3x I3y I3z')
    I1 = sp.Matrix([[I1x, 0, 0],
                    [0, I1y, 0],
                    [0, 0, I1z]])

    I2 = sp.Matrix([[I2x, 0, 0],
                    [0, I2y, 0],
                    [0, 0, I2z]])

    I3 = sp.Matrix([[I3x, 0, 0],
                    [0, I3y, 0],
                    [0, 0, I3z]])
   
    K1 = 1/2*(m1*v1.T*v1 + w1.T*I1*w1)
    K2 = 1/2*(m2*v2.T*v2 + w2.T*I2*w2)
    Ktotal = K1 + K2


    print_kinematics = False
    
    if print_kinematics:
        print("\n\nKinematikk ledd 1:\n")
        sp.pprint(K1)
        
        print("\n\nKinematikk ledd 2:\n")
        sp.pprint(K2)
        
        print("\n\nTotal kinematikk, K\N{SUBSCRIPT ONE} + K\N{SUBSCRIPT TWO}:\n")
        sp.pprint(K)
        
    h1, h2, h3 = 0, 0, 0
    P1 = h1*m1*g
    P2 = h2*m2*g
    P3 = h3*m3*g
    
    Ptotal = sp.Matrix([P1 + P2])

    Lagrangian = Ktotal - Ptotal    
    
    qt1, qt2, qt3 = dynamicsymbols('theta1 theta2 theta3')
    dt1, dt2, dt3 = dynamicsymbols('d1 d2 d3')
    
    "Sett inn variabler som funksjon av tiden slik at man kan derivere den riktig"
    Lagrangian = Lagrangian.subs(q1, qt1)
    Lagrangian = Lagrangian.subs(d2, dt2)
    


    
    "FYLL INN"
    q_liste = sp.Matrix([qt1, dt1]) # Liste med hvilke leddvariabler som inngår i manipulatoren

    torque1, torque2 = torque(Lagrangian, q_liste, q_dot)
    

       
if __name__ == '__main__':
    main(None)