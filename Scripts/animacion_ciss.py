import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc
import os
import time

# Para las gráficas de LaTex
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
N_electrones = 500  # Número total de electrones
N_pasos = 100  # Número de iteraciones de Monte Carlo
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

# Diferencia de potencial por unidad de longitud
dV = V / N_posiciones  # Voltaje por paso

# Valores de q_CISS para los cuales vamos a realizar la simulación
q_CISS_values = np.linspace(0, 1, 10)  # Variar q_CISS de 0 a 1 (10 valores)

# Crear una carpeta para guardar los gráficos
os.makedirs('results/evolucion_espines_q_ciss', exist_ok=True)

# Inicialización de la distribución de electrones
def inicializar_distribucion():
    distribucion = [[] for _ in range(N_posiciones)]
    for _ in range(N_electrones):
        posicion = np.random.randint(0, N_posiciones//10)  # 10% inicial
        espin = np.random.choice([-1, 1])  # Asignar espín aleatorio
        distribucion[posicion].append(espin)
    return distribucion

# Simulación de difusión para un valor específico de q_CISS
def simular(q_CISS):
    distribucion = inicializar_distribucion()
    spines_drenados_up = 0
    spines_drenados_down = 0
    historial_spines_up = []
    historial_spines_down = []

    for _ in range(N_pasos):
        nueva_distribucion = [[] for _ in range(N_posiciones)]
        for i in range(N_posiciones):
            mov_electrones = int(D * len(distribucion[i]))

            for _ in range(mov_electrones):
                if distribucion[i]:
                    espin = distribucion[i].pop()
                    P_der_mod = 1 / (1 + np.exp(- (dV + q_CISS * dV * espin) / (kB * T)))
                    rand = np.random.rand()

                    if rand < P_der_mod and i + 1 < N_posiciones:  # Movimiento hacia la derecha
                        if i + 1 == N_posiciones - 1:  # Si llega al drain
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

    return historial_spines_up, historial_spines_down

# Generar y guardar gráficos para cada valor de q_CISS
for i, q_CISS in enumerate(q_CISS_values):
    historial_spines_up, historial_spines_down = simular(q_CISS)

    # Graficar la polarización de espín para este valor de q_CISS
    plt.figure(figsize=(8, 5))
    plt.plot(range(N_pasos), historial_spines_up, label="Espines Up", color='r')
    plt.plot(range(N_pasos), historial_spines_down, label="Espines Down", color='b')
    plt.xlabel("Paso de tiempo")
    plt.ylabel("Electrones drenados")
    plt.title(f"Evolución de espines en el drain\npara $q_{{\\mathrm{{CISS}}}} = {q_CISS:.2f}$")
    plt.legend()

    # Guardar el gráfico
    plt.savefig(f'results/evolucion_espines_q_ciss/q_ciss_{i}.png')
    plt.close()

print(f"Gráficos guardados en 'results/evolucion_espines_q_ciss'")

# Lista de imágenes
imagenes = [f'results/evolucion_espines_q_ciss/q_ciss_{i}.png' for i in range(len(q_CISS_values))]

# Crear la animación
fig, ax = plt.subplots(figsize=(8, 5))

# Configurar los ejes una vez, solo al principio
ax.set_axis_off()  # Para ocultar los ejes

# Cargar la primera imagen
img = plt.imread(imagenes[0])
im = ax.imshow(img)

def actualizar(frame):
    img = plt.imread(imagenes[frame])  # Cargar la siguiente imagen
    im.set_data(img)  # Actualizar la imagen mostrada
    return [im]

# Configuración de la animación
ani = animation.FuncAnimation(fig, actualizar, frames=len(imagenes), interval=500, blit=True)

# Guardar la animación como GIF
os.makedirs('results', exist_ok=True)
ani.save('results/evolucion_espines_qciss_animation.gif', writer='pillow')

plt.show()
