import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from matplotlib import rc
import time  # Importar el módulo time

# Configuración de estilo LaTeX para las gráficas
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
L = 30  # Número de posiciones en el cable
N_electrones = 100  # Número total de electrones
pasos = 200  # Número de iteraciones de Monte Carlo
D = 1  # Coeficiente de difusión
T = 300  # Temperatura en Kelvin
V = 0.001  # Diferencia de potencial (Voltios)
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1  # Carga del electrón

# Inicialización: electrones concentrados en un extremo
distribucion = np.zeros(L)
distribucion[:L//10] = N_electrones / (L//10)
# distribucion[15] = N_electrones


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

print('Probabilidad derecha: ', P_der, 'Probabilidad izquierda: ', P_izq)

# Iniciar el cronómetro para todo el proceso
start_time = time.time()  # Tiempo de inicio

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
print(f"Corriente medida: {I:.2e} A")

# Crear animación
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, L-2)
ax.set_ylim(0, max(map(max, historial)) * 1.1)
ax.set_xlabel("Posición en el cable")
ax.set_ylabel("Densidad de electrones")
tiempo_text = ax.text(0.8 * L, max(map(max, historial)) * 1.05, '', fontsize=12)
ax.set_title("Evolución de la distribución electrónica")
line, = ax.plot([], [], 'bo-', markersize=4)

def actualizar(frame):
    tiempo_text.set_text(f'N_steps = {frame}')
    line.set_data(range(L), historial[frame])
    return line, tiempo_text

ani = animation.FuncAnimation(fig, actualizar, frames=pasos, interval=50, blit=True)

# Guardar animación
os.makedirs('results', exist_ok=True)
ani.save('results/transporte_electrones.gif', writer='pillow')

# Finalizar el cronómetro después de todo el proceso
end_time = time.time()  # Tiempo de finalización
execution_time = end_time - start_time  # Calcular el tiempo de ejecución

# Convertir el tiempo de ejecución en horas, minutos y segundos
hours, remainder = divmod(execution_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Tiempo total de ejecución: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")

plt.show()
