class Nodo:
    
    def __init__(self, estado, profundidad, profundidadObjetivo, padre, puntosAcumuladosIa, puntosAcumuladosJugador, movimiento, casillasPuntos, turno, casillasObtenidasIA, casillasObtenidasJugador, resultado):
        self.estado = estado
        self.profundidad = profundidad
        self.profundidadObjetivo = profundidadObjetivo
        self.padre = padre
        self.puntosAcumuladosIa = puntosAcumuladosIa
        self.puntosAcumuladosJugador = puntosAcumuladosJugador
        self.movimiento = movimiento
        self.casillasPuntos = casillasPuntos
        self.turno = turno
        self.casillasObtenidasIA = casillasObtenidasIA
        self.casillasObtenidasJugador = casillasObtenidasJugador
        self.resultado = resultado
    
    def get_padre(self):
        return self.padre
    
    def get_estado(self):
        return self.estado
    
    def get_turno(self):
        return self.turno
    
    def get_casillas_puntos(self):
        return self.casillasPuntos
    
    def get_profundidad(self):
        return self.profundidad
    
    def get_movimiento(self):
        return self.movimiento

    def get_puntos_ia(self):
        return self.puntosAcumuladosIa
    
    def get_puntos_jugador(self):
        return self.puntosAcumuladosJugador
        
    def resultadoHeuristica(self):
        resultado = 0
        if (self.puntosAcumuladosIa > self.puntosAcumuladosJugador and self.casillasPuntos == 0 and self.casillasObtenidasIA > self.casillasObtenidasJugador):
            resultado = float('inf')
            
        elif (self.puntosAcumuladosIa < self.puntosAcumuladosJugador and self.casillasPuntos == 0 and self.casillasObtenidasIA < self.casillasObtenidasJugador):
            resultado = float('-inf')
        else:
            resultado = (self.puntosAcumuladosIa + self.casillasObtenidasIA) - (self.puntosAcumuladosJugador + self.casillasObtenidasJugador)
            
        if (resultado == 0 and self.profundidadObjetivo == 2):
            IAo  = ubicarElemento(self.estado, '10')
            x = IAo[0]
            y = IAo[1]
            oponente = ubicarElemento(self.estado, '9')
            xo = oponente[0]
            yo = oponente[1]
            
            resultado = (contar_movimientos_en_L(self.estado, (x-1, y-1)) - contar_movimientos_en_L(self.estado,(xo, yo)))
            
        self.resultado = resultado
    
    def set_resultado(self, resultado):
        self.resultado = resultado
        
    def get_resultado(self):
        return self.resultado
    
def encontrar_posicion_mayor(coordenadas, matriz):
    numeros = ['1', '2', '3', '4', '5', '6', '7']
    maximo = float('-inf')  # Inicializar con un valor muy bajo

    for coord in coordenadas:
        fila, columna = coord
        elemento = matriz[fila-1][columna-1]
        if elemento in numeros:
            numero = int(elemento)
            if numero > maximo:
                maximo = numero
                
    return maximo

def ubicarElemento (matriz, elementoabuscar):
    coordenadas = []
    for fila in matriz:
        for elemento in fila:
            if elemento == elementoabuscar:
                coordenadas.append(matriz.index(fila))
                coordenadas.append(fila.index(elemento))
                return coordenadas
    return -1

def contar_movimientos_en_L(matriz, coordenada):
    filas = len(matriz)
    columnas = len(matriz[0])
    fila, columna = coordenada

    # Verificar si la coordenada está dentro de los límites de la matriz
    if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
        return -1  # Valor de retorno para indicar una coordenada inválida

    # Definir los posibles movimientos en L del caballo
    movimientos = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    # Inicializar una matriz de distancias con valores infinitos
    distancias = [[float('inf')] * columnas for _ in range(filas)]

    # Establecer la distancia a la coordenada inicial como 0
    distancias[fila][columna] = 0

    # Crear una cola para realizar un recorrido BFS (Breadth-First Search)
    cola = [(fila, columna)]

    while cola:
        x, y = cola.pop(0)

        # Comprobar los movimientos posibles desde la posición actual
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy

            # Verificar si la nueva posición está dentro de los límites de la matriz
            if 0 <= nx < filas and 0 <= ny < columnas:
                # Calcular la distancia a la nueva posición
                nueva_distancia = distancias[x][y] + 1

                # Actualizar la distancia si es menor que la distancia almacenada actualmente
                if nueva_distancia < distancias[nx][ny]:
                    distancias[nx][ny] = nueva_distancia
                    cola.append((nx, ny))

    # Encontrar la ficha más cercana y obtener la distancia correspondiente
    distancia_minima = float('inf')
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] in ['1', '2', '3', '4', '5', '6', '7']:
                distancia_minima = min(distancia_minima, distancias[i][j])

    # Si no se encontró ninguna ficha, retornar -1
    if distancia_minima == float('inf'):
        return -1

    return distancia_minima
