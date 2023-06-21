import copy
from nodo import Nodo

def ubicarElemento (matriz, elementoabuscar):
    coordenadas = []
    for fila in matriz:
        for elemento in fila:
            if elemento == elementoabuscar:
                coordenadas.append(matriz.index(fila)+1)
                coordenadas.append(fila.index(elemento)+1)
                return coordenadas
    return -1

def buscar_numero(coordenadas, matriz, casillasPuntos, turno):
    actualizacionCasillas = casillasPuntos
    matriz_aux = copy.deepcopy(matriz)
    puntosObtenidosIA = 0
    puntosObtenidosJugador = 0
    x, y = coordenadas
    numero = matriz_aux[x-1][y-1]
    valor = int(numero)
    if 1 <= valor <= 7:
        if (turno == 0):
            puntosObtenidosIA += valor
            actualizacionCasillas -= 1
            ubicacion = ubicarElemento(matriz, '10')
            matriz_aux[ubicacion[0]-1][ubicacion[1]-1] = '0'
            matriz_aux[x-1][y-1] = '10'
        else:
            puntosObtenidosJugador += valor
            actualizacionCasillas -= 1
            ubicacion = ubicarElemento(matriz, '9')
            matriz_aux[ubicacion[0]-1][ubicacion[1]-1] = '0'
            matriz_aux[x-1][y-1] = '9'
    else:
        if (turno == 0):
            ubicacion = ubicarElemento(matriz, '10')
            matriz_aux[ubicacion[0]-1][ubicacion[1]-1] = '0'
            matriz_aux[x-1][y-1] = '10'
        else:
            ubicacion = ubicarElemento(matriz, '9')
            matriz_aux[ubicacion[0]-1][ubicacion[1]-1] = '0'
            matriz_aux[x-1][y-1] = '9'
    return puntosObtenidosIA, puntosObtenidosJugador, matriz_aux, actualizacionCasillas

def movimientosPosibles(turno, estado):
    
    movimientos = []
    
    if (turno == 0):
        ubicacion = ubicarElemento(estado, '10')
    else:
        ubicacion = ubicarElemento(estado, '9')
        
    fila = ubicacion[0]
    columna = ubicacion[1]
    
    movimientos_posibles = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for movimiento in movimientos_posibles:
        
        filaFinal = fila + movimiento[0]
        columnaFinal = columna + movimiento[1]
        
        if (filaFinal >= 1 and filaFinal <= 7 and columnaFinal >= 1 and columnaFinal <= 7):
            if (turno == 0):
                ubicacionRival = ubicarElemento(estado, '9')
                if ((ubicacionRival[0],ubicacionRival[1]) != (filaFinal, columnaFinal)):
                    movimientos.append((filaFinal, columnaFinal))
            else:
                ubicacionRival = ubicarElemento(estado, '10')
                if ((ubicacionRival[0],ubicacionRival[1]) != (filaFinal, columnaFinal)):
                    movimientos.append((filaFinal, columnaFinal))
             
    return movimientos

def crearArbol (nodo, turno, profundidadFinal, listaNodos):
    if (nodo.get_profundidad() < profundidadFinal ):
        for movimiento in movimientosPosibles(turno, nodo.get_estado()):
            
            #se hace copia de la matriz que se tiene hasta el momento
            matriz_aux = copy.deepcopy(nodo.get_estado())
            
            #se hace copia de los puntajes que se tienen hasta el momento
            movimientosAcumuladosIa = nodo.get_puntos_ia()
            movimientosAcumuladosJugador = nodo.get_puntos_jugador()
            
            #se inicializa la variable que determina el turno
            proximoTurno = None
            
            #se hace el movimiento y se cuentan los puntos obtenidos para el turno correspondiente
            
            puntosObtenidosIA, puntosObtenidosJugador, matriz_modificada, casillas = buscar_numero(movimiento, matriz_aux, nodo.get_casillas_puntos(), turno)
            
            movimientosAcumuladosIa += puntosObtenidosIA
            movimientosAcumuladosJugador += puntosObtenidosJugador
            
            if (turno == 0):
                proximoTurno = 1
            else:
                proximoTurno = 0
                
            #se crea el hijo con los nuevos datos obtenidos
            hijo = Nodo(matriz_modificada, nodo.get_profundidad() +1, profundidadFinal, nodo, movimientosAcumuladosIa, movimientosAcumuladosJugador,movimiento, casillas, turno, None)
            
            #si se llega a la profundida se calcula el valor de la heuristica
            if (hijo.get_profundidad() == profundidadFinal):
                hijo.resultadoHeuristica()
                
            #se agrega el nodo hijo creado a lista total de nodos
            listaNodos[nodo.get_profundidad()].append(hijo)
            
            #se crean los hijos de cada movimiento
            crearArbol(hijo, proximoTurno, profundidadFinal, listaNodos)

def recorrerArbol(profundidad, arrayNodos):
    
    #hay que tener en cuenta que los nodos de profundidad n estan guardados en la posicion n-1 de la matriz de nodos
    
    movimientoEscogido = None
    
    for i in range(profundidad-1, -1, -1):
        
        #si la profundidad es par, los padres obtendran el valor minimo de los nodos de esa profundidad, en caso contrario, obtendran el valor maximo
        
        if ((i+1) % 2 == 0):
            obtenerMax = False
        else:
            obtenerMax = True
        
        if (i != 0):
            
            for nodoPadre in arrayNodos[i-1]:  #se obtienen los padres  
                
                #se obtienen los hijos de esos padres
                nodosHijo = [nodo for nodo in arrayNodos[i] if nodo.get_padre() == nodoPadre]
            
                #asignar el resultado a cada padre
                if obtenerMax:
                    nodoPadre.set_resultado(max(nodosHijo, key=lambda hijo: hijo.get_resultado()).get_resultado())
                else:
                    nodoPadre.set_resultado(min(nodosHijo, key=lambda hijo: hijo.get_resultado()).get_resultado())
                    
        else: #si se llega a la profundidad final, se asigna el max al nodo padre
            movimientoEscogido = max(arrayNodos[0], key=lambda hijo: hijo.get_resultado()).get_movimiento()
            
    return movimientoEscogido 