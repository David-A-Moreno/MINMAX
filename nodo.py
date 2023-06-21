class Nodo:
    
    def __init__(self, estado, profundidad, profundidadObjetivo, padre, puntosAcumuladosIa, puntosAcumuladosJugador, movimiento, casillasPuntos, turno, resultado=None):
        self.estado = estado
        self.profundidad = profundidad
        self.profundidadObjetivo = profundidadObjetivo
        self.padre = padre
        self.puntosAcumuladosIa = puntosAcumuladosIa
        self.puntosAcumuladosJugador = puntosAcumuladosJugador
        self.movimiento = movimiento
        self.casillasPuntos = casillasPuntos
        self.turno = turno
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
        if (self.puntosAcumuladosIa > self.puntosAcumuladosJugador and self.casillasPuntos == 0):
            resultado = float('inf')
            
        elif (self.puntosAcumuladosIa < self.puntosAcumuladosJugador and self.casillasPuntos == 0):
            resultado = float('-inf')
        else:
            resultado = self.puntosAcumuladosIa - self.puntosAcumuladosJugador
            
        self.resultado = resultado
    
    def set_resultado(self, resultado):
        self.resultado = resultado
        
    def get_resultado(self):
        return self.resultado
