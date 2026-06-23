import cv2
import numpy as np
import os
import argparse

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

def ver_frambuesas(video_path, carpeta_salida, tiempo_inicial, intervalo):
    cap = cv2.VideoCapture(video_path)

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duracion_segundos = total_frames / fps


    segundos_objetivo = list(range(tiempo_inicial, int(duracion_segundos), intervalo))

    frames_objetivo = [int(seg * fps) for seg in segundos_objetivo]

    frame_actual_idx = 0

    while cap.isOpened():
        exito, frame = cap.read()
        if not exito:
            break  
        
        if frame_actual_idx in frames_objetivo:
            segundo_exacto = segundos_objetivo[frames_objetivo.index(frame_actual_idx)]
            print(f"-> Procesando y guardando frame del segundo: {segundo_exacto}s (Frame {frame_actual_idx})")
            
            img = frame[100:, 450:-350]
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (170, 40, 60), (180, 255, 255))
            
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                perimeter = cv2.arcLength(cnt, True)
                circularidad = (4 * np.pi * area) / (perimeter**2) if perimeter > 0 else 0
                
                # Filtro inteligente
                if 100 < area < 5000 and circularidad > 0.25:
                    # 1. Centro de masa
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                    else:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cx = x + w // 2
                        cy = y + h // 2
                    
                    x_min, y_min = cx - 50, cy - 50
                    x_max, y_max = cx + 50, cy + 50
                    
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
                    
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    cv2.circle(img, (cx, cy), 3, (0, 0, 255), -1)
            
            nombre_archivo = os.path.join(carpeta_salida, f"frambuesas_segundo_{segundo_exacto}.jpg")
            cv2.imwrite(nombre_archivo, img)
            
        frame_actual_idx += 1

    cap.release()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Script de Machine Vision para detectar y recortar frambuesas en un video."
    )

    # Definimos los argumentos que aceptará la terminal
    parser.add_argument("-v", "--video", type=str, required=True, 
                        help="Ruta del archivo de video (ej: video.mp4)")
    
    parser.add_argument("-o", "--output", type=str, default="resultado_frambuesas", 
                        help="Carpeta donde se guardarán las imagenes con las cajitas")
    
    parser.add_argument("-t", "--inicio", type=int, default=0, 
                        help="Segundo inicial del video para empezar a procesar (Por defecto: 0)")
    
    parser.add_argument("-i", "--intervalo", type=int, default=1, 
                        help="Intervalo de tiempo en segundos para analizar frames (Por defecto: 1)")

    args = parser.parse_args()

    ver_frambuesas(
        video_path=args.video, 
        carpeta_salida=args.output, 
        tiempo_inicial=args.inicio, 
        intervalo=args.intervalo
    )