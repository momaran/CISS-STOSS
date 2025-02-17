import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from matplotlib import rc
import time

# Configuración de estilo LaTeX para las gráficas
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
N_electrones = 500  # Número total de electrones
N_pasos = 200  # Número de iteraciones de Monte Carlo
N_moleculas = N_electrones
D = 1    # Coeficiente de difusión
T = 300  # Temperatura en Kelvin
V = 0.1  # Diferencia de potencial (Voltios)
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1.602e-19  # Carga del electrón en Culombios 

# Parámetros físicos
total_length = 2e-9  # Longitud total del sistema en metros (2 nm)
N_posiciones = 15  # Número de pasos espaciales
dx = total_length / N_posiciones  # Longitud de un paso en metros
dt = 1e-9/(6*D*N_posiciones)  # Paso de tiempo en segundos

# Inicialización: electrones concentrados en un extremo con distribución de espines
distribucion = [[] for _ in range(N_posiciones)]
for _ in range(N_electrones):
    posicion = np.random.randint(0, N_posiciones//10)  # 10% inicial
    espin = np.random.choice([-1, 1])  # Asignar espín aleatorio
    distribucion[posicion].append(espin)

# Contadores de electrones drenados
electrones_drenados = 0
spines_drenados_up = 0
spines_drenados_down = 0

# Diferencia de potencial por unidad de longitud
dV = V / N_posiciones  # Voltaje por paso

# Valores de q_CISS para los cuales vamos a realizar la simulación
q_CISS_values = np.linspace(0, 1, N_pasos)  # Variar q_CISS de 0 a 1 durante los pasos
historial_spines_up = []
historial_spines_down = []

# Iniciar el cronómetro para todo el proceso
start_time = time.time()

# Simulación para diferentes valores de q_CISS
for q_CISS in q_CISS_values:
    # Resetear la distribución de electrones y los contadores
    distribucion = [[] for _ in range(N_posiciones)]
    spines_drenados_up = 0
    spines_drenados_down = 0

    for _ in range(N_electrones):
        posicion = np.random.randint(0, N_posiciones//10)  # 10% inicial
        espin = np.random.choice([-1, 1])  # Asignar espín aleatorio
        distribucion[posicion].append(espin)
    
    # Simulación de difusión para este valor de q_CISS
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

                    if rand < P_der_mod and i + 1 < N_posiciones:  # Movimiento hacia la derecha
                        if i + 1 == N_posiciones - 1:  # Si llega al drain
                            electrones_drenados += 1
                            if espin == 1:
                                spines_drenados_up += 1
                            else:
                                spines_drenados_down += 1
                            nueva_distribucion[0].append(espin)  # Vuelve a la posición inicial (contorno circular)
                        else:
                            nueva_distribucion[i + 1].append(espin)
                    elif rand < 1 and i - 1 >= 0:  # Movimiento hacia la izquierda
                        nueva_distribucion[i - 1].append(espin)
                    else:
                        nueva_distribucion[i].append(espin)  # Si no se mueve, se mantiene en la misma posición

        distribucion = nueva_distribucion
        historial_spines_up.append(spines_drenados_up)
        historial_spines_down.append(spines_drenados_down)

# Crear animación del gráfico de polarización
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, N_pasos-1)
ax.set_ylim(0, max(max(historial_spines_up), max(historial_spines_down)) * 1.1)
ax.set_xlabel("Paso de tiempo")
ax.set_ylabel("Electrones drenados")
tiempo_text = ax.text(0.7 * N_pasos, max(max(historial_spines_up), max(historial_spines_down)) * 1.05, '', fontsize=12)
plt.subplots_adjust(right=0.75)

parametros_texto = (
    rf"$V = {V}$ V" "\n"
    rf"$T = {T}$ K" "\n"
    rf"$D = {D}$" "\n"
    rf"$N_{{\mathrm{{pasos}}}} = {N_pasos}$" "\n"
    rf"$N_{{\mathrm{{electrones}}}} = {N_electrones}$"
)
plt.figtext(0.8, 0.5, parametros_texto, fontsize=12, va="center", bbox=dict(facecolor='white', alpha=0.8))
ax.set_title("Evolución de la polarización de espín para distintos valores de q_CISS")

line_up, = ax.plot([], [], label="Espines Up", color='r')
line_down, = ax.plot([], [], label="Espines Down", color='b')

def actualizar(frame):
    q_ciss_val = q_CISS_values[frame]
    tiempo_text.set_text(f'q_CISS = {q_ciss_val:.2f}')
    line_up.set_data(range(frame + 1), historial_spines_up[:frame + 1])
    line_down.set_data(range(frame + 1), historial_spines_down[:frame + 1])
    return line_up, line_down, tiempo_text

ani = animation.FuncAnimation(fig, actualizar, frames=N_pasos, interval=100, blit=True)
os.makedirs('results', exist_ok=True)
ani.save('results/animacion_ciss.gif', writer='pillow')

# Finalizar el cronómetro después de todo el proceso
end_time = time.time()
execution_time = end_time - start_time

hours, remainder = divmod(execution_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Tiempo total de ejecución: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")
plt.show()
