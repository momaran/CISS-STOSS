# config.py - Contiene los parámetros de la simulación
import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Parámetros de la simulación
N_electrones = 1000  # Número total de electrones
N_pasos = 5000  # Número de iteraciones de Monte Carlo
D = 0.9    # Coeficiente de difusión
T = 300  # Temperatura en Kelvin
V = 0.1  # Diferencia de potencial (Voltios)
kB = 8.617e-5  # Constante de Boltzmann en eV/K
q = 1.602e-19  # Carga del electrón en Culombios
q_ciss = 1 #carga del CISS.

# Parámetros físicos
total_length = 2e-9  # Longitud total del sistema en metros (2 nm)
N_posiciones = 15  # Número de pasos espaciales
dx = total_length / N_posiciones  # Longitud de un paso en metros
dt = 1e-9/(6*D*N_posiciones)  # Paso de tiempo en segundos

# Diferencia de potencial por unidad de longitud
dV = V / N_posiciones  # Voltaje por paso
