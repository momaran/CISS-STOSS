import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from matplotlib import rc

# Configuración de estilo LaTeX
rc("text", usetex=True)
rc("font", family="serif")

# Parámetros de la simulación
L = 30  # Número de posiciones en el cable
N_electrones = 100  # Número total de electrones
pasos = 100  # Número de iteraciones
D = 0.4  # Coeficiente de difusión (reducido para estabilidad)

# Inicialización: electrones en un extremo
distribucion = np.zeros(L)
distribucion[:L//10] = N_electrones / (L//10)

# Simulación de difusión conservativa
historial = [distribucion.copy()]
for _ in range(pasos):
    nueva_distribucion = distribucion.copy()
    flujo = np.zeros(L-1)  # Flujo entre sitios contiguos

    # Calcular flujo entre posiciones contiguas
    for i in range(L-1):
        flujo[i] = D * (distribucion[i] - distribucion[i+1])

    # Aplicar flujo de manera conservativa
    for i in range(1, L-1):
        nueva_distribucion[i] += flujo[i-1] - flujo[i]

    # Verificar conservación total
    nueva_distribucion[0] += -flujo[0]  # Mantener balance en el borde izquierdo
    nueva_distribucion[-1] += flujo[-1]  # Mantener balance en el borde derecho

    # Normalizar para evitar errores numéricos
    factor = N_electrones / np.sum(nueva_distribucion)
    nueva_distribucion *= factor

    distribucion = nueva_distribucion.copy()
    historial.append(distribucion.copy())

# Crear animación
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, L)
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
ani.save('results/difusion_electrones.gif', writer='pillow')
plt.show()
