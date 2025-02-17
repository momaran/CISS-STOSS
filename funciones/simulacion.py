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