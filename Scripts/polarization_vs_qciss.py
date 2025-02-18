import numpy as np
import matplotlib.pyplot as plt
from funciones.simulacion import simular

# Valores de q_CISS utilizados en la simulación
q_CISS_values = np.linspace(0, 1, 100)

# Lista para almacenar la polarización final de cada simulación
polarizacion_final = []

# Ejecutar las simulaciones para cada q_CISS y obtener la última polarización
# Ejecutar las simulaciones para cada q_CISS y obtener la última polarización
for q_CISS in q_CISS_values:
    _, _, historial_polarizacion = simular(q_CISS)
    polarizacion_final.append(historial_polarizacion[-1])  # Tomamos el último valor de polarización

# Graficar Polarización vs q_CISS
plt.figure(figsize=(8, 5))
plt.plot(q_CISS_values, polarizacion_final, marker='o', linestyle='-', color='b')

# Configurar etiquetas y formato LaTeX
plt.xlabel(r"$q_{\mathrm{CISS}}$")
plt.ylabel("Polarización final")
plt.title(r"Polarización final en función de $q_{\mathrm{CISS}}$")
plt.grid(True)

# Guardar la gráfica
plt.savefig("results/polarizacion_vs_q_ciss.png")
plt.show()