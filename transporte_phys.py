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
N_electrones = 100  # Número total de electrones
N_pasos = 50  # Número de iteraciones de Monte Carlo
D = 1    # Coeficiente de difusión (a determinar en unidades correctas)
T = 300  # Temperatura en Kelvin
V = 0.1  # Diferencia de potencial (Voltios)
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1.602e-19  # Carga del electrón en Culombios 

# Parámetros físicos
total_length = 2e-9  # Longitud total del sistema en metros (2 nm)
N_posiciones = 30  # Número de pasos espaciales
dx = total_length / N_posiciones  # Longitud de un paso en metros
dt = 1e-9/(6*D*N_posiciones)  # Paso de tiempo en segundos

# Inicialización: electrones concentrados en un extremo
# distribucion = np.zeros(N_posiciones)
# distribucion[:N_posiciones//10] = N_electrones / (N_posiciones//10)
distribucion = np.full(N_posiciones, N_electrones / N_posiciones)

# Simulación de difusión con temperatura y potencial
electrones_drenados = 0  # Contador de electrones que llegan al extremo derecho

# Diferencia de potencial por unidad de longitud
dV = V / N_posiciones  # Voltaje por paso 

# Probabilidades de transición basadas en Boltzmann
P_der = 1 / (1 + np.exp(-dV / (kB * T))) #dV en electronvoltios
P_izq = 1 - P_der

print('Probabilidad derecha: ', P_der, 'Probabilidad izquierda: ', P_izq)

# Iniciar el cronómetro para todo el proceso
start_time = time.time()

historial = [distribucion.copy()]

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
    historial.append(distribucion.copy())

# Calcular corriente promedio en Amperios
I = q * (electrones_drenados / (N_pasos* dt))
print(f"Corriente medida: {I:.2e} A")

# Crear animación
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, N_posiciones-2)
ax.set_ylim(0, max(map(max, historial)) * 1.1)
ax.set_xlabel("Posición en el cable")
ax.set_ylabel("Densidad de electrones")
tiempo_text = ax.text(0.8 * N_posiciones, max(map(max, historial)) * 1.05, '', fontsize=12)
ax.set_title("Evolución de la distribución electrónica")
line, = ax.plot([], [], 'bo-', markersize=4)

def actualizar(frame):
    tiempo_text.set_text(f'N_steps = {frame}')
    line.set_data(range(N_posiciones), historial[frame])
    return line, tiempo_text

ani = animation.FuncAnimation(fig, actualizar, frames=N_pasos, interval=50, blit=True)

# Guardar animación
os.makedirs('results', exist_ok=True)
ani.save('results/transporte_electrones.gif', writer='pillow')

# Finalizar el cronómetro después de todo el proceso
end_time = time.time()
execution_time = end_time - start_time

hours, remainder = divmod(execution_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Tiempo total de ejecución: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")

plt.show()
