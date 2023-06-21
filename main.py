import tkinter as tk
from tkinter import ttk
from funciones import crearArbol, recorrerArbol, movimientosPosibles, buscar_numero
from nodo import Nodo
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import os
import random

ventana = tk.Tk()

def generar_matriz():
    matriz = [['0' for _ in range(7)] for _ in range(7)]
    numeros = ['1', '2', '3', '4', '5', '6', '7', '9', '10']
    random.shuffle(numeros)
    
    for num in numeros:
        fila = random.randint(0, 6)
        columna = random.randint(0, 6)
        
        while matriz[fila][columna] != '0':
            fila = random.randint(0, 6)
            columna = random.randint(0, 6)
        
        matriz[fila][columna] = num
    
    return matriz

matriz = generar_matriz()

casillasFaltantes = 7
puntaje_ia = 0
puntaje_jugador = 0
dificultad = -1
    
# Obtener el ancho y la altura de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
altura_pantalla = ventana.winfo_screenheight()

# Calcular la posición x e y de la ventana para centrarla
x = int((ancho_pantalla - 900) / 2)  # ancho de la ventana es 800
y = int((altura_pantalla - 450) / 2)  # altura de la ventana es 600

# Configurar la posición de la ventana
ventana.geometry(f"900x450+{x}+{y}")

# Calcular el tamaño de cada celda
cell_width = 450 // 7
cell_height = 450 // 7

# Crear el canvas
canvas = tk.Canvas(ventana, width=450, height=450)
canvas.pack()

coordenadas = movimientosPosibles('1', matriz)

def hover_enter(event):
        button = event.widget
        button.config(bg="gray")  # Cambiar el fondo a gris
        
def hover_leave(event):
        button = event.widget
        button.config(bg="white")
        
def comprobar_ganador(puntaje_ia, puntaje_jugador):
    if(puntaje_ia > puntaje_jugador):
        show_result_message(1)
    elif(puntaje_ia < puntaje_jugador):
        show_result_message(2)
    else:
        show_result_message(0)
    
        
def on_button_click(row, col, matriz, puntaje_jugador, puntaje_ia, casillasFaltantes, nodosTotales):
    
    global dificultad
    
    puntosObtenidosIA, puntosObtenidosJugador, matriz_modificada, casillas = buscar_numero((row+1, col+1), matriz, casillasFaltantes, 1)
    
    puntaje_jugador += puntosObtenidosJugador
    casillasFaltantes = casillas
    matriz = matriz_modificada
    
    actualizar_botones(matriz, puntaje_jugador, puntaje_jugador, casillasFaltantes, nodosTotales)
    actualizar_puntajes(puntaje_ia, puntaje_jugador)
    
    if (casillasFaltantes == 0):
        comprobar_ganador(puntaje_ia, puntaje_jugador)
        return
    
    nodosTotales.clear()
    nodosTotales = [[] for _ in range(dificultad)]
    padre = Nodo(matriz,0,dificultad,None,puntaje_ia,puntaje_jugador,None,casillasFaltantes, None,None)
    crearArbol(padre, 0, dificultad , nodosTotales)
    movimiento = recorrerArbol(dificultad, nodosTotales)
    
    puntosObtenidosIA, puntosObtenidosJugador, matriz_modificada, casillas = buscar_numero(movimiento, matriz, casillasFaltantes, 0)
    
    puntaje_ia += puntosObtenidosIA
    casillasFaltantes = casillas
    matriz = matriz_modificada
    
    actualizar_botones(matriz, puntaje_jugador, puntaje_ia, casillasFaltantes, nodosTotales)
    actualizar_puntajes(puntaje_ia, puntaje_jugador)
    
    if (casillasFaltantes == 0):
        comprobar_ganador(puntaje_ia, puntaje_jugador)
        return

# Crear la matriz de botones
buttons = []
for row in range(7):
    button_row = []
    for col in range(7):
        numero = matriz[row][col]  # Obtener el número correspondiente a la posición en la matriz
        
        # Calcular las coordenadas de la celda
        x0 = col * cell_width
        y0 = row * cell_height
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        
        # Crear un botón desactivado por defecto
        button = tk.Button(canvas, width=cell_width, height=cell_height, state=tk.DISABLED, relief=tk.SOLID)
        
        image = Image.open("./imagenes/white.png") 
        
        if numero == '1':
            image = Image.open("./imagenes/1.png")  
        
        elif numero == '2':
            image = Image.open("./imagenes/2.png")  
            
        elif numero == '3':
            image = Image.open("./imagenes/3.png")
            
        elif numero == '4':
            image = Image.open("./imagenes/4.png")
        
        elif numero == '5':
            image = Image.open("./imagenes/5.png")
            
        elif numero == '6':
            image = Image.open("./imagenes/6.png")
            
        elif numero == '7':
            image = Image.open("./imagenes/7.png")
            
        elif numero == '9':
            image = Image.open("./imagenes/negro.png")
            
        elif numero == '10':
            image = Image.open("./imagenes/blanco.png")
            
        image = image.resize((cell_width, cell_height))  # Redimensionar la imagen al tamaño del botón
        photo = ImageTk.PhotoImage(image)
        button.config(image=photo)
        button.image = photo
        
        # Colocar el botón en el canvas utilizando el método place
        button.place(x=x0, y=y0, width=cell_width, height=cell_height)
        
        button_row.append(button)
    
    buttons.append(button_row)
    
btn = tk.Button(ventana, text='Empezar', bg='blue', fg='white', font=("Arial", 12))         
btn.place(x=710,y=350, width=150, height=50)
btn.config(command=lambda: [mostrar_dropdown(), destroyButton()])

def startGame(dificultadSeleccionada, matriz, puntaje_jugador, puntaje_ia, casillasFaltantes):
    
    
    global dificultad
    dificultad = dificultadSeleccionada
    
    nodosTotales = [[] for _ in range(dificultadSeleccionada)]
    padre = Nodo(matriz,0,dificultadSeleccionada,None,puntaje_ia,puntaje_jugador,None,casillasFaltantes, None,None)
    crearArbol(padre, 0, dificultadSeleccionada, nodosTotales)
    movimiento = recorrerArbol(dificultadSeleccionada, nodosTotales)
    
    puntosObtenidosIA, puntosObtenidosJugador, matriz_modificada, casillas = buscar_numero(movimiento, matriz, casillasFaltantes, 0)
    
    
    puntaje_ia += puntosObtenidosIA
    puntaje_jugador += puntosObtenidosJugador
    casillasFaltantes = casillas
    matriz = matriz_modificada
    
    if (casillasFaltantes == 0):
        comprobar_ganador(puntaje_ia, puntaje_jugador)
        return
    
    actualizar_botones(matriz, puntaje_jugador, puntaje_ia, casillasFaltantes, nodosTotales)
    actualizar_puntajes(puntaje_ia, puntaje_jugador)
    
def destroyButton():
    btn.destroy()

def actualizar_botones(matriz, puntaje_jugador, puntaje_ia, casillasFaltantes, nodosTotales):
    for row in range(7):
        for col in range(7):
            button = buttons[row][col]  # Obtener el botón correspondiente a la posición en la matriz
            button.unbind("<Enter>")
            button.unbind("<Leave>")
            button.unbind("<Button-1>")
            button.config(bg="white")
    coordenadas = movimientosPosibles('1', matriz)
    for row in range(7):
        for col in range(7):
            numero = matriz[row][col]  # Obtener el número correspondiente a la posición en la matriz
            button = buttons[row][col]  # Obtener el botón correspondiente a la posición en la matriz
            
            image = Image.open("./imagenes/white.png") 
            
            if numero == '1':
                image = Image.open("./imagenes/1.png")
                
            elif numero == '2':
                image = Image.open("./imagenes/2.png")
                
            elif numero == '3':
                image = Image.open("./imagenes/3.png")
                
            elif numero == '4':
                image = Image.open("./imagenes/4.png")
                
            elif numero == '5':
                image = Image.open("./imagenes/5.png")
                
            elif numero == '6':
                image = Image.open("./imagenes/6.png")
                
            elif numero == '7':
                image = Image.open("./imagenes/7.png")
                
            elif numero == '9':
                image = Image.open("./imagenes/negro.png")
                
            elif numero == '10':
                image = Image.open("./imagenes/blanco.png")
                
            image = image.resize((cell_width, cell_height))
            photo = ImageTk.PhotoImage(image)
            button.config(image=photo)
            button.image = photo
            for coordenada in coordenadas:
                if coordenada == (row+1, col+1):
                    button.bind("<Enter>", hover_enter)
                    button.bind("<Leave>", hover_leave)
                    button.bind("<Button-1>", lambda event, row=row, col=col: on_button_click(row, col, matriz, puntaje_jugador, puntaje_ia, casillasFaltantes, nodosTotales))

# Labels de puntajes
puntaje_ia_label = tk.Label(ventana, text=f"Puntaje IA: {puntaje_ia}", font=("Arial", 15))
puntaje_ia_label.place(x=10, y=10)

puntaje_jugador_label = tk.Label(ventana, text=f"Puntaje Jugador: {puntaje_jugador}" , font=("Arial", 15))
puntaje_jugador_label.place(x=710, y=10)

def actualizar_puntajes(puntaje_ia, puntaje_jugador):
    puntaje_ia_label.config(text=f"Puntaje IA: {puntaje_ia}")
    puntaje_jugador_label.config(text=f"Puntaje Jugador: {puntaje_jugador}")
    
def mostrar_dropdown():
    dificultadSeleccionada = 2

    def seleccionar_opcion():
        nonlocal dificultadSeleccionada
        selected_option = dropdown.get()
        if selected_option == "principiante":
            dificultadSeleccionada = 2
        elif selected_option == "amateur":
            dificultadSeleccionada = 4
        elif selected_option == "experto":
            dificultadSeleccionada = 6

    ventana = tk.Tk()
    ventana.geometry("250x150")
    ventana.title("Seleccione nivel")

    titulo = tk.Label(ventana, text="Seleccione nivel", font=("Arial", 12, "bold"), width=20, height=2)
    titulo.pack(pady=10)

    opciones = ["principiante", "amateur", "experto"]

    dropdown = ttk.Combobox(ventana, values=opciones, state="readonly")
    dropdown.current(0)  # Establecer la opción predeterminada
    dropdown.bind("<<ComboboxSelected>>", lambda event: seleccionar_opcion())
    dropdown.pack()

    # Botón "Aceptar"
    def cerrar_ventana():
        ventana.destroy()
        destroyButton()
        
    global casillasFaltantes
    casillas = casillasFaltantes

    boton_aceptar = tk.Button(ventana, text="Aceptar", command=cerrar_ventana)
    boton_aceptar.config(command=lambda: [startGame(dificultadSeleccionada, matriz, puntaje_jugador, puntaje_ia, casillas), cerrar_ventana()])
    boton_aceptar.pack(pady=20)

    # Centrar la ventana en la pantalla
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")

    ventana.mainloop()
    
    
def show_result_message(resultado):
    # Crear una ventana emergente (messagebox)
    result_message = tk.Toplevel()
    result_message.title("Resultado")

    # Determinar el texto del mensaje según el ganador
    if resultado == 1:
        message = "¡Ganó la IA!"
    elif resultado == 2:
        message = "¡Ganaste!"
    else:
        message = "¡Empate!"

    # Mostrar el mensaje
    label = tk.Label(result_message, text=message)
    label.pack(padx=80, pady=20)

    # Función para reiniciar el juego
    def play_again():
        # Cerrar la ventana emergente
        result_message.destroy()
        ventana.destroy()
        os.system("python main.py")

    # Crear el botón "Jugar de nuevo"
    play_again_button = tk.Button(result_message, text="Jugar de nuevo", command=play_again)
    play_again_button.pack(padx=20, pady=10)
    
    result_message.update_idletasks()
    width = result_message.winfo_width()
    height = result_message.winfo_height()
    x = (result_message.winfo_screenwidth() // 2) - (width // 2)
    y = (result_message.winfo_screenheight() // 2) - (height // 2)
    result_message.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    result_message.deiconify()
        
ventana.mainloop()
