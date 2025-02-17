import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# Configuración de estilo LaTeX para las gráficas
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
N_electrones = 100  # Número total de electrones
N_moleculas = N_electrones  # Número de moléculas en paralelo
N_pasos = 300  # Número de iteraciones de Monte Carlo
D = 1  # Coeficiente de difusión 
T = 300  # Temperatura en Kelvin
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1.602e-19  # Carga del electrón en Culombios 

# Parámetros físicos
total_length = 2e-9  # Longitud total del sistema en metros (2 nm)
N_posiciones = 10  # Número de pasos espaciales
dx = total_length / N_posiciones  # Longitud de un paso en metros
dt = 1e-9 / (6 * D * N_posiciones)  # Paso de tiempo en segundos

# Diferentes valores de voltaje para los que calcular la corriente
voltajes = np.linspace(0.01, 0.2, 100)  # Rango de voltajes
intensidades = []  # Lista para guardar las intensidades de corriente

for V in voltajes:
    distribucion = np.full(N_posiciones, N_electrones / N_posiciones)
    electrones_drenados = 0  # Contador de electrones que llegan al extremo derecho
    dV = V / N_posiciones  

    # Probabilidades de transición basadas en Boltzmann
    P_der = 1 / (1 + np.exp(-dV / (kB * T)))
    P_izq = 1 - P_der

    for _ in range(N_pasos):
        nueva_distribucion = distribucion.copy()
        for i in range(N_posiciones):
            if distribucion[i] > 0:
                mov = int(D * distribucion[i])
                for _ in range(mov):
                    rand = np.random.rand()
                    if rand < P_der and i + 1 < N_posiciones:
                        nueva_distribucion[i] -= 1
                        nueva_distribucion[i + 1] += 1
                        if i + 1 == N_posiciones - 1:
                            electrones_drenados += 1
                            nueva_distribucion[i + 1] -= 1  
                            nueva_distribucion[0] += 1  
                    elif rand < P_der + P_izq and i - 1 >= 0:
                        nueva_distribucion[i] -= 1
                        nueva_distribucion[i - 1] += 1
        
        distribucion = nueva_distribucion.copy()

    # Calcular corriente promedio
    I = q * N_moleculas * (electrones_drenados / (N_pasos * dt)) * 1e9  # nA
    intensidades.append(I)

# Graficar la curva I-V
plt.figure(figsize=(8, 6))
plt.plot(voltajes, intensidades, 'bo', markersize=6, label="Datos simulados")  # Se asegura de incluir la leyenda
plt.xlabel(r'Voltaje (V)', fontsize=14)
plt.ylabel(r'Corriente (nA)', fontsize=14)
plt.title(r'Curva Característica I-V', fontsize=16)
plt.grid(True)
plt.legend(fontsize=12, loc='upper left', frameon=True)  # Se fuerza a que la leyenda aparezca

# Ajustar el espacio para dejar sitio a la derecha
plt.subplots_adjust(right=0.75)  # Mueve la gráfica a la izquierda

# Definir texto con parámetros
parametros_texto = (
    rf"$T = {T}$ K" "\n"
    rf"$D = {D}$" "\n"
    rf"$N_{{\mathrm{{pasos}}}} = {N_pasos}$" "\n"
    rf"$N_{{\mathrm{{electrones}}}} = {N_electrones}$"
)

# Mostrar el texto en la parte derecha
plt.figtext(0.8, 0.5, parametros_texto, fontsize=12, va="center", bbox=dict(facecolor='white', alpha=0.8))
plt.show()
