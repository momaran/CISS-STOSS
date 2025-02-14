import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# Configuración de estilo LaTeX para las gráficas
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
L = 30  # Número de posiciones en el cable
N_electrones = 100  # Número total de electrones
pasos = 400  # Número de iteraciones de Monte Carlo
D = 0.5  # Coeficiente de difusión
T = 300  # Temperatura en Kelvin
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1  # Carga del electrón

# Diferentes valores de voltaje para los que calcular la corriente
voltajes = np.linspace(0.01, 1, 10000)  # Voltajes entre 0.1 y 5 V
intensidades = []  # Lista para guardar las intensidades de corriente

for V in voltajes:
    # Inicialización: electrones concentrados en un extremo
    distribucion = np.zeros(L)
    distribucion[:L//10] = N_electrones / (L//10)

    # Simulación de difusión con temperatura y potencial
    historial = [distribucion.copy()]
    electrones_drenados = 0  # Contador de electrones que llegan al extremo derecho

    # Diferencia de potencial por unidad de longitud
    dV = V / L  

    # Energía de transición considerando el potencial
    dE_der = q * dV  # Energía para moverse a la derecha

    # Probabilidades de transición basadas en Boltzmann
    P_der = 1 / (1 + np.exp(-dE_der / (kB * T)))
    P_izq = 1 - P_der

    for _ in range(pasos):
        nueva_distribucion = distribucion.copy()
        for i in range(L):  # Incluir bordes
            if distribucion[i] > 0:
                
                # Número de electrones que intentan moverse (difusión base)
                mov = int(D * distribucion[i])
                
                for _ in range(mov):
                    rand = np.random.rand()
                    if rand < P_der and i + 1 < L:
                        nueva_distribucion[i] -= 1
                        nueva_distribucion[i + 1] += 1
                        if i + 1 == L - 1:
                            electrones_drenados += 1
                            nueva_distribucion[i + 1] -= 1  # Remover electrón del drain
                            nueva_distribucion[0] += 1  # Reinsertar en el inicio
                    elif rand < P_der + P_izq and i - 1 >= 0:
                        nueva_distribucion[i] -= 1
                        nueva_distribucion[i - 1] += 1
        
        distribucion = nueva_distribucion.copy()
        historial.append(distribucion.copy())

    # Calcular corriente promedio
    I = q * (electrones_drenados / pasos)
    intensidades.append(I)  # Guardar la intensidad correspondiente a este voltaje

# Graficar la curva I-V
plt.figure(figsize=(8, 6))
plt.plot(voltajes, intensidades, 'bo', markersize=6)
plt.xlabel(r'Voltaje (V)', fontsize=14)
plt.ylabel(r'Corriente (A)', fontsize=14)
plt.title(r'Curva Característica I-V', fontsize=16)
plt.grid(True)
plt.show()
