import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from matplotlib import rc
import time

# Configuración de estilo LaTeX
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
N_electrones = 1000
N_pasos = 200
N_moleculas = N_electrones
D = 0.5
T = 300
V = 0.1
kB = 8.617e-5
q = 1.602e-19
q_CISS = 1

# Parámetros físicos
total_length = 2e-9
N_posiciones = 15
dx = total_length / N_posiciones
dt = 1e-9 / (6 * D * N_posiciones)

# Inicialización
distribucion = [[] for _ in range(N_posiciones)]
for _ in range(N_electrones):
    posicion = np.random.randint(0, N_posiciones // 10)
    espin = np.random.choice([-1, 1])
    distribucion[posicion].append(espin)

# Contadores de electrones drenados
electrones_drenados = 0
spines_drenados_up = 0
spines_drenados_down = 0

dV = V / N_posiciones

historial_polarizacion = []

start_time = time.time()

# Simulación
for _ in range(N_pasos):
    nueva_distribucion = [[] for _ in range(N_posiciones)]
    for i in range(N_posiciones):
        mov_electrones = int(D * len(distribucion[i]))
        for _ in range(mov_electrones):
            if distribucion[i]:
                espin = distribucion[i].pop()
                P_der_mod = 1 / (1 + np.exp(- (dV + q_CISS * dV * espin) / (kB * T)))
                P_izq = 1 - P_der_mod
                rand = np.random.rand()
                
                if rand < P_der_mod and i + 1 < N_posiciones:
                    if i + 1 == N_posiciones - 1:
                        electrones_drenados += 1
                        if espin == 1:
                            spines_drenados_up += 1
                        else:
                            spines_drenados_down += 1
                        nueva_distribucion[0].append(espin)
                    else:
                        nueva_distribucion[i + 1].append(espin)
                elif rand < 1 and i - 1 >= 0:
                    nueva_distribucion[i - 1].append(espin)
                else:
                    nueva_distribucion[i].append(espin)
    
    # Aplicar la condición de contorno circular para el lado izquierdo
    nueva_distribucion[N_posiciones - 1].extend(nueva_distribucion[0])
    nueva_distribucion[0] = []
    
    distribucion = nueva_distribucion
    
    # Calcular polarización en cada posición
    polarizacion = []
    for pos in distribucion:
        up = pos.count(1)
        down = pos.count(-1)
        if up + down > 0:
            polarizacion.append((up - down) / (up + down))
        else:
            polarizacion.append(0)
    historial_polarizacion.append(polarizacion)

# Crear animación de mapa de calor
fig, ax = plt.subplots()
cmap = plt.get_cmap("bwr")
cbar = None

def actualizar(frame):
    ax.clear()
    im = ax.imshow([historial_polarizacion[frame]], cmap=cmap, aspect='auto', vmin=-1, vmax=1)
    ax.set_xlabel("Posición en el cable")
    ax.set_xticks(range(N_posiciones))
    ax.set_yticks([])
    ax.set_title(f"Paso {frame}")
    global cbar
    if cbar is None:
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Polarización")
    return im,

ani = animation.FuncAnimation(fig, actualizar, frames=N_pasos, interval=50, blit=False)
os.makedirs('results', exist_ok=True)
ani.save('results/transporte_espines.gif', writer='pillow')

# Tiempo de ejecución
end_time = time.time()
execution_time = end_time - start_time
hours, remainder = divmod(execution_time, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"Tiempo total de ejecución: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")
plt.show()
