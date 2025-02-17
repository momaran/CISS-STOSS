import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os

# Configuración de estilo LaTeX para las gráficas
from matplotlib import rc
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
N_electrones = 500  # Número total de electrones
N_pasos = 600  # Número de iteraciones de Monte Carlo
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
q_CISS_values = np.linspace(0, 1, 100)  # Variar q_CISS de 0 a 1 (10 valores)

# Crear una carpeta para guardar los gráficos
os.makedirs('results/polarizacion_q_ciss', exist_ok=True)

# Iniciar el cronómetro para todo el proceso
start_time = time.time()

# Inicialización de la distribución de electrones
def inicializar_distribucion():
    distribucion = [[] for _ in range(N_posiciones)]
    for _ in range(N_electrones):
        posicion = np.random.randint(0, N_posiciones)  # 10% inicial
        espin = np.random.choice([-1, 1])  # Asignar espín aleatorio
        distribucion[posicion].append(espin)
    return distribucion

# Simulación de difusión para un valor específico de q_CISS
def simular(q_CISS):
    distribucion = inicializar_distribucion()
    spines_drenados_up = 0
    spines_drenados_down = 0
    historial_polarizacion = []

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

        # Calcular la polarización
        if spines_drenados_up + spines_drenados_down > 0:
            polarizacion = (spines_drenados_up - spines_drenados_down) / (spines_drenados_up + spines_drenados_down)
        else:
            polarizacion = 0

        historial_polarizacion.append(polarizacion)

    return historial_polarizacion

# Generar y guardar gráficos para cada valor de q_CISS
for i, q_CISS in enumerate(q_CISS_values):
    historial_polarizacion = simular(q_CISS)

    # Eliminar los primeros 25 pasos para evitar el ruido transitorio
    historial_polarizacion_recortado = historial_polarizacion[25:]

    # Obtener el último valor de polarización
    ultima_polarizacion = historial_polarizacion_recortado[-1] if historial_polarizacion_recortado else 0

    # Graficar la polarización en función del paso de tiempo (desde el paso 25)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(25, N_pasos), historial_polarizacion_recortado, color='b')
    
    # Ajustar los límites del eje y entre 0 y 1
    ax.set_ylim(0, 1)
    
    # Escribir el valor de la última polarización en el borde derecho
    ax.text(N_pasos - 10, ultima_polarizacion, f"{ultima_polarizacion:.2f}", fontsize=12, verticalalignment='center', horizontalalignment='right')

    # Etiquetas y título
    ax.set_xlabel("Paso de tiempo")
    ax.set_ylabel("Polarización")
    ax.set_title(f"Polarización de espín en función del paso de tiempo\npara $q_{{\\mathrm{{CISS}}}} = {q_CISS:.2f}$")

    # Guardar el gráfico
    plt.savefig(f'results/polarizacion_q_ciss/polarizacion_{i}.png')
    plt.close()

print(f"Gráficos guardados en 'results/polarizacion_q_ciss'")

# Lista de imágenes generadas
imagenes = [f'results/polarizacion_q_ciss/polarizacion_{i}.png' for i in range(len(q_CISS_values))]

# Crear la animación
fig, ax = plt.subplots(figsize=(8, 5))

# Cargar la primera imagen
img = plt.imread(imagenes[0])
im = ax.imshow(img)

# Eliminar los ejes para que no se dibujen
ax.axis('off')

def actualizar(frame):
    img = plt.imread(imagenes[frame])
    im.set_data(img)
    return [im]

# Configuración de la animación
ani = animation.FuncAnimation(fig, actualizar, frames=len(imagenes), interval=500, blit=True)

# Guardar la animación como GIF
os.makedirs('results', exist_ok=True)
ani.save('results/polarizacion_q_ciss_animation.gif', writer='pillow', fps=2)

# Finalizar el cronómetro después de todo el proceso
end_time = time.time()
execution_time = end_time - start_time

hours, remainder = divmod(execution_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Tiempo total de ejecución: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")

plt.show()
