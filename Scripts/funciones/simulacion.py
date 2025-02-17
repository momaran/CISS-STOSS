# simulacion.py - Contiene la función para simular la evolución de los electrones
import numpy as np
from funciones.config import N_pasos, N_posiciones, D, dV, kB, T
from funciones.inicializar import inicializar_distribucion
import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def simular(q_CISS):
    """
    Simula la evolución de los electrones en el sistema considerando el efecto CISS.
    
    Args:
        q_CISS (float): Parámetro que modula la asimetría en la difusión de espines.
    
    Returns:
        tuple: Dos listas con el historial de espines drenados up y down en cada paso de tiempo,
               y la lista de polarización final.
    """
    distribucion = inicializar_distribucion()
    spines_drenados_up = 0
    spines_drenados_down = 0
    historial_spines_up = []
    historial_spines_down = []
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
        historial_spines_up.append(spines_drenados_up)
        historial_spines_down.append(spines_drenados_down)

        # Calcular la polarización en cada paso
        if spines_drenados_up + spines_drenados_down > 0:
            polarizacion = (spines_drenados_up - spines_drenados_down) / (spines_drenados_up + spines_drenados_down)
        else:
            polarizacion = 0  # Si no hay electrones drenados, la polarización es 0
        historial_polarizacion.append(polarizacion)

    return historial_spines_up, historial_spines_down, historial_polarizacion
