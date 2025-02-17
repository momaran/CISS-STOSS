# funciones/inicializar.py
import numpy as np
from funciones.config import N_posiciones, N_electrones
import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def inicializar_distribucion() -> list[list[int]]:
    """
    Inicializa la distribución de electrones en el sistema.

    Returns:
        list[list[int]]: Lista de listas donde cada índice representa una posición y contiene una lista de espines.
    """
    distribucion = [[] for _ in range(N_posiciones)]
    for _ in range(N_electrones):
        posicion = np.random.randint(0, N_posiciones)  # Posición inicial aleatoria
        espin = np.random.choice([-1, 1])  # Espín aleatorio (+1 o -1)
        distribucion[posicion].append(espin)
    return distribucion
