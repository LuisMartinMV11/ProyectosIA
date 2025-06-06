import pygame
import random
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego de Salto y Esquiva")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, menu, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None
modelo = None  # Modelo de árbol de decisión
modelo_knn = None  # Modelo KNN (opcional, si decides usarlo)


# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
nave_arriba = pygame.Rect(jugador.x, jugador.y - 64, 64, 64)  # Nueva nave arriba del jugador
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

pelota_nave = pygame.Rect(jugador.x, 0, 16, 16)  # Pelotita lanzada desde la nave de arriba
velocidad_pelota_nave = 0
pelota_en_caida = False

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Nueva variable para controlar si el jugador está esquivando a la izquierda
esquivando_izquierda = False
regresando = False
posicion_inicial = 50  # X inicial del jugador
posicion_izquierda = 10  # X a la que se mueve para esquivar
movio_izquierda = False  # Indica si el jugador se movió a la izquierda

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2, nave_arriba
    global pelota_nave, velocidad_pelota_nave, pelota_en_caida

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # La nave de arriba siempre está fija en la parte superior, alineada con la posición inicial del jugador
    nave_arriba.x = posicion_inicial - 16  # Centrar la nave sobre la posición inicial del jugador
    nave_arriba.y = 0  # Siempre arriba

    # Lanzar la pelotita si no está cayendo
    if not pelota_en_caida:
        pelota_nave.x = nave_arriba.x + (nave_arriba.width // 2) - 8  # Centrar respecto a la nave
        pelota_nave.y = nave_arriba.y + nave_arriba.height
        velocidad_pelota_nave = gravedad
        pelota_en_caida = True

    # Mover la pelotita si está cayendo
    if pelota_en_caida:
        pelota_nave.y += velocidad_pelota_nave
        pantalla.blit(bala_img, (pelota_nave.x, pelota_nave.y))  # Puedes usar otra imagen si quieres

        # Colisión entre la pelotita y el jugador
        if jugador.colliderect(pelota_nave):
            print("¡Colisión con la pelotita de la nave!")
            reiniciar_juego()

        # Si la pelotita llega al suelo, reiniciar
        if pelota_nave.y > h:
            pelota_en_caida = False

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave_img, (nave_arriba.x, nave_arriba.y))  # Dibuja la nueva nave arriba del jugador

def lanzar_pelota_nave():
    global pelota_nave, velocidad_pelota_nave, pelota_en_caida
    pelota_nave.x = nave_arriba.x + (nave_arriba.width // 2) - 8  # Centrar la pelotita respecto a la nave
    pelota_nave.y = nave_arriba.y + nave_arriba.height
    velocidad_pelota_nave = gravedad  # Velocidad igual a la gravedad
    pelota_en_caida = True

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto, pelota_nave, movio_izquierda
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    distancia_pelota_arriba = abs(jugador.x - pelota_nave.x)
    movio_izquierda_val = 1 if movio_izquierda else 0
    # Guardar velocidad de la bala, distancia al jugador, si saltó, distancia a la pelotita de arriba y si se movió a la izquierda
    datos_modelo.append((velocidad_bala, distancia, salto_hecho, distancia_pelota_arriba, movio_izquierda_val))

#  Función para entrenar el modelo de árbol de decisión
def entrenar_modelo():
    global modelo

    if not datos_modelo:
        print("No hay datos para entrenar el modelo.")
        modelo = None
        return

    columnas = ['velocidad_bala', 'distancia_bala', 'salto', 'distancia_pelota_arriba', 'movio_izquierda']
    df = pd.DataFrame(datos_modelo, columns=columnas)
    X = df[['velocidad_bala', 'distancia_bala', 'distancia_pelota_arriba', 'movio_izquierda']]
    y = df[['salto', 'movio_izquierda']]
    modelo = DecisionTreeClassifier()
    modelo.fit(X, y)
    print("Modelo entrenado y listo para jugar automáticamente.")

# entrener el modelo KNN (opcional)
def entrenar_modelo_knn(k=3):
    global modelo_knn

    if not datos_modelo:
        print("No hay datos para entrenar el modelo.")
        modelo_knn = None
        return

    # Convertir la lista de datos en un DataFrame
    columnas = ['velocidad_bala', 'distancia_bala', 'salto', 'distancia_pelota_arriba', 'movio_izquierda']
    df = pd.DataFrame(datos_modelo, columns=columnas)

    # Variables predictoras (X) y variable objetivo (y)
    X = df[['velocidad_bala', 'distancia_bala', 'distancia_pelota_arriba', 'movio_izquierda']]
    y = df[['salto', 'movio_izquierda']]

    # Crear y entrenar el modelo KNN
    modelo_knn = KNeighborsClassifier(n_neighbors=k)
    modelo_knn.fit(X, y)
    print(f"Modelo KNN entrenado con k={k}")

# Función para entrenar un modelo de red neuronal
def entrenar_modelo_nn():
    global modelo_nn, scaler 

    if not datos_modelo:
        print("No hay datos para entrenar el modelo.")
        modelo_nn = None
        return
    # Convertir la lista de datos en un DataFrame
    columnas = ['velocidad_bala', 'distancia_bala', 'salto', 'distancia_pelota_arriba', 'movio_izquierda']
    df = pd.DataFrame(datos_modelo, columns=columnas)
    # Variables predictoras (X) y variable objetivo (y)
    X = df[['velocidad_bala', 'distancia_bala', 'distancia_pelota_arriba', 'movio_izquierda']]
    y = df[['salto', 'movio_izquierda']]

    # Escalar las características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Crear y entrenar el modelo de red neuronal
    modelo_nn = MLPClassifier(hidden_layer_sizes=(5, 5), max_iter=1000)
    modelo_nn.fit(X_scaled, y)
    print("Modelo de red neuronal entrenado y listo para jugar automáticamente.")

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, datos_modelo
    global modelo, modelo_knn, modelo_nn, scaler

    opciones = [
        ("Auto (A)", pygame.K_a),
        ("Manual (M)", pygame.K_m),
        ("K vecinos (K)", pygame.K_k),
        ("Red neuronal (N)", pygame.K_n),
        ("Salir (Q)", pygame.K_q)
    ]
    ancho_boton = 320
    alto_boton = 50
    espacio = 20
    botones = []

    pantalla.fill(NEGRO)
    titulo = fuente.render("Selecciona el modo de juego:", True, BLANCO)
    pantalla.blit(titulo, (w // 2 - titulo.get_width() // 2, h // 2 - 180))

    for i, (texto, _) in enumerate(opciones):
        x = w // 2 - ancho_boton // 2
        y = h // 2 - 80 + i * (alto_boton + espacio)
        rect = pygame.Rect(x, y, ancho_boton, alto_boton)
        botones.append((rect, texto))
    
    while menu_activo:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill(NEGRO)
        pantalla.blit(titulo, (w // 2 - titulo.get_width() // 2, h // 2 - 180))

        for i, (rect, texto) in enumerate(botones):
            color = (70, 130, 180) if rect.collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(pantalla, color, rect, border_radius=10)
            pygame.draw.rect(pantalla, BLANCO, rect, 2, border_radius=10)
            texto_render = fuente.render(texto, True, BLANCO)
            pantalla.blit(texto_render, (rect.x + (ancho_boton - texto_render.get_width()) // 2,
                                         rect.y + (alto_boton - texto_render.get_height()) // 2))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                for i, (_, key) in enumerate(opciones):
                    if evento.key == key:
                        if key == pygame.K_a:
                            modo_auto = True
                            entrenar_modelo()
                            modelo_knn = None
                            modelo_nn = None
                            scaler = None
                            menu_activo = False
                        elif key == pygame.K_k:
                            modo_auto = True
                            entrenar_modelo_knn(k=3)
                            modelo = None
                            modelo_nn = None
                            scaler = None
                            menu_activo = False
                        elif key == pygame.K_n:
                            modo_auto = True
                            entrenar_modelo_nn()
                            modelo = None
                            modelo_knn = None
                            menu_activo = False
                        elif key == pygame.K_m:
                            modo_auto = False
                            modelo = None
                            modelo_knn = None
                            modelo_nn = None
                            scaler = None
                            datos_modelo = []
                            menu_activo = False
                        elif key == pygame.K_q:
                            print("Juego terminado. Datos recopilados:", datos_modelo)
                            pygame.quit()
                            exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, (rect, _) in enumerate(botones):
                    if rect.collidepoint(mouse_pos):
                        key = opciones[i][1]
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    global pelota_nave, velocidad_pelota_nave, pelota_en_caida, nave_arriba
    global esquivando_izquierda, regresando, movio_izquierda  # <-- agrega aquí

    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True

    # Reiniciar la pelotita de la nave de arriba
    pelota_nave.x = nave_arriba.x + (nave_arriba.width // 2) - 8
    pelota_nave.y = nave_arriba.y + nave_arriba.height
    velocidad_pelota_nave = gravedad
    pelota_en_caida = False

    # REINICIA ESTADO DE MOVIMIENTO
    esquivando_izquierda = False
    regresando = False
    movio_izquierda = False

    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def main():
    global salto, en_suelo, bala_disparada, esquivando_izquierda, regresando, movio_izquierda

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    prev_jugador_x = jugador.x  # <-- Guarda la posición anterior del jugador

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    if not esquivando_izquierda and jugador.x == posicion_inicial:
                        jugador.x = posicion_izquierda
                        esquivando_izquierda = True
                        regresando = False
                if evento.key == pygame.K_UP and en_suelo and not pausa:
                    # Permitir saltar si está en la posición inicial o si ya se movió a la izquierda
                    if jugador.x == posicion_inicial or esquivando_izquierda:
                        salto = True
                        en_suelo = False
                        # Solo activar regreso si saltó desde la izquierda
                        if esquivando_izquierda:
                            regresando = True
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto y el movimiento lateral
            if not modo_auto:
                if salto:
                    manejar_salto()
                    guardar_datos()  # Ya guardas cada frame de salto

                # Guardar cada frame mientras está esquivando a la izquierda
                if jugador.x == posicion_izquierda:
                    movio_izquierda = True
                    guardar_datos()
                else:
                    movio_izquierda = False

                # Cuando termina el salto y debe regresar
                if regresando and not salto and en_suelo and jugador.x != posicion_inicial:
                    jugador.x = posicion_inicial
                    esquivando_izquierda = False
                    regresando = False

                prev_jugador_x = jugador.x  # Actualiza la posición anterior

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        if modo_auto:
            if (modelo is not None or modelo_knn is not None or modelo_nn is not None) and en_suelo:
                distancia = abs(jugador.x - bala.x)
                distancia_pelota_arriba = abs(jugador.x - pelota_nave.x)
                movio_izquierda_val = 1 if jugador.x == posicion_izquierda else 0
                entrada = [[velocidad_bala, distancia, distancia_pelota_arriba, movio_izquierda_val]]

                if modelo_knn is not None:
                    prediccion = modelo_knn.predict(entrada)[0]
                elif modelo_nn is not None:
                    # Recuerda escalar la entrada igual que en el entrenamiento
                    X = np.array(entrada)
                    X_scaled = scaler.transform(X)
                    prediccion = modelo_nn.predict(X_scaled)[0]
                else:
                    prediccion = modelo.predict(entrada)[0]

                pred_salto = prediccion[0]
                pred_izquierda = prediccion[1]

                # Guardar el dato justo cuando el modelo decide esquivar a la izquierda
                if pred_izquierda == 1 and jugador.x == posicion_inicial:
                    movio_izquierda = True
                    guardar_datos()
                    jugador.x = posicion_izquierda
                    esquivando_izquierda = True
                    regresando = False
                else:
                    movio_izquierda = False

                # Guardar el dato cuando el modelo decide saltar
                if pred_salto == 1 and en_suelo:
                    salto = True
                    en_suelo = False
                    guardar_datos()
                    if esquivando_izquierda:
                        regresando = True

            # Manejo del salto y regreso automático
            if salto:
                manejar_salto()
            if regresando and not salto and en_suelo and jugador.x != posicion_inicial:
                jugador.x = posicion_inicial
                regresando = False

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
