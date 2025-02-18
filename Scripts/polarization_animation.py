import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from funciones.simulacion import simular
import time
import os
from funciones.config import N_pasos

# Configuración de estilo LaTeX para las gráficas
from matplotlib import rc
rc("text", usetex=True)
rc("font", family="serif")

# Valores de q_CISS para los cuales vamos a realizar la simulación
q_CISS_values = np.linspace(0, 1, 100)  # Variar q_CISS de 0 a 1 (10 valores)

# Crear una carpeta para guardar los gráficos
os.makedirs('results/polarizacion_q_ciss', exist_ok=True)

# Iniciar el cronómetro para todo el proceso
start_time = time.time()

# Generar y guardar gráficos para cada valor de q_CISS
for i, q_CISS in enumerate(q_CISS_values):
    _,_,historial_polarizacion = simular(q_CISS)

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