import cv2
import numpy as np
import os
import argparse

def computer_vision(video_path, carpeta_salida, tiempo_inicial, intervalo):
        #Silencia mensajes de salida de algunos comandos de cv2, aunque el codigo funciona correctamente
        os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

        #Cargamos el video y lo leemos con openCV
        cap = cv2.VideoCapture(video_path)

        #En caso de no existir se crea la carpeta de salida
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)
        
        #Vemos los fps del video y el numero total de frames para saber su duración
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duracion_segundos = total_frames / fps

        print(f"Procesando desde el segundo {tiempo_inicial} cada {intervalo} segundos...")

        #Obteniendo una lista con todos los frames requeridos
        segundos_objetivo = list(range(tiempo_inicial, int(duracion_segundos), intervalo))
        frames_objetivo = [int(seg * fps) for seg in segundos_objetivo]

        #Indice del bucle
        frame_actual_idx = 0

        #bucle de lectura secuencial para los frames
        while cap.isOpened():
            #vemos si capturo la imagen correctamente y leemos el frame
            exito, frame = cap.read()
            if not exito:
                break
            #si el indice esta dentro
            if frame_actual_idx in frames_objetivo:
                segundo_exacto = segundos_objetivo[frames_objetivo.index(frame_actual_idx)]
                
                # aplicamos un recorte en este caso para la cinta transportadora (modificable)
                img = frame[100:, 450:-350]
                
                #transformamos la imagen de BGR (el original) a formato HSV, luego aplicamos una mascara blanco y negro
                #los parametros de la mascara en nuestro caso se obtuvieron a mano utilizando detecta_color.py

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, (170, 40, 60), (180, 255, 255))
                
                #aplicamos 2 pequeños filtros morfologicos con un kernerl de 5x5, el OPEN tiñe los pequeños puntos blancos aislados
                #el CLOSE aplica lo contrario, rellena partes negras para completar la forma de las frambuesas
                kernel = np.ones((5,5), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
                #extraemos los contornos de las frambuesas
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #Contador para diferenciar las frambuesas que aparezcan en el mismo segundo
                contador_fruta = 0
                
                #detectamos los parametros fundamentales, area, perimetro, circularidad utilizando los contornos
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    perimeter = cv2.arcLength(cnt, True)
                    circularidad = (4 * np.pi * area) / (perimeter**2) if perimeter > 0 else 0
                    


                    #aplicamos un filtro de area y circularidad, esto elimina objetos grandes o muy pequeños (trozos de frambuesa o la cinta)
                    #que pueda haber detectado, tambien elimina los objetos que tienen muy baja circularidad, para no detectar la cinta

                    if 100 < area < 5000 and circularidad > 0.25:
                        #encuentra el centro de masa de cada frambuesa utilizando sus momentos

                        M = cv2.moments(cnt)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                        #si falla lo hace de manera más manual pero menos precisa utilizando su ancho y largo
                        else:
                            x, y, w, h = cv2.boundingRect(cnt)
                            cx = x + w // 2
                            cy = y + h // 2
                        

                        #para tener imagenes de 100x100 calculamos los bordes
                        y_min, y_max = cy - 50, cy + 50
                        x_min, x_max = cx - 50, cx + 50
                        
                        # esta parte es un ajuste para que no falle el codigo, porque si la frambuesa esta muy fuera de los limites
                        # el codigo fallaba, esto detecta si se sale del maximo de la imagen y se ajusta
                        alto_img, ancho_img = img.shape[:2]
                        
                        if y_min < 0:
                            y_max = min(alto_img, y_max - y_min)
                            y_min = 0
                        if x_min < 0:
                            x_max = min(ancho_img, x_max - x_min)
                            x_min = 0
                        if y_max > alto_img:
                            y_min = max(0, y_min - (y_max - alto_img))
                            y_max = alto_img
                        if x_max > ancho_img:
                            x_min = max(0, x_min - (x_max - ancho_img))
                            x_max = ancho_img

                        
                        #Ahora cortamos la imagen con los limites calculados
                        recorte_frambuesa = img[y_min:y_max, x_min:x_max]
                        
                        #verifica que la imagen si quedo de 100x100
                        if recorte_frambuesa.shape[0] == 100 and recorte_frambuesa.shape[1] == 100:
                            contador_fruta += 1
                            
                            #guarda la imagen de la frambuesa
                            nombre_archivo = os.path.join(
                                carpeta_salida, 
                                f"fruta_seg_{segundo_exacto}_num_{contador_fruta}.jpg"
                            )
                            cv2.imwrite(nombre_archivo, recorte_frambuesa)
                            
                print(f"guardadas {contador_fruta} frambuesas del segundo {segundo_exacto}s")
            #sumamos al indice de frame para que siga corriendo    
            frame_actual_idx += 1
        #cerramos el video cuando termina
        cap.release()



#creamos un main para poder usarlo de terminal
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Script de Machine Vision para detectar y recortar frambuesas en un video."
    )

    # Definimos los argumentos que aceptará la terminal
    parser.add_argument("-v", "--video", type=str, required=True, 
                        help="Ruta del archivo de video (ej: video.mp4)")
    
    parser.add_argument("-o", "--output", type=str, default="resultado_frambuesas", 
                        help="Carpeta donde se guardarán los recortes (Por defecto: 'resultado_frambuesas')")
    
    parser.add_argument("-t", "--inicio", type=int, default=0, 
                        help="Segundo inicial del video para empezar a procesar (Por defecto: 0)")
    
    parser.add_argument("-i", "--intervalo", type=int, default=1, 
                        help="Intervalo de tiempo en segundos para analizar frames (Por defecto: 1)")

    args = parser.parse_args()

    computer_vision(
        video_path=args.video, 
        carpeta_salida=args.output, 
        tiempo_inicial=args.inicio, 
        intervalo=args.intervalo
    )