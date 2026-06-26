import cv2
import numpy as np
import argparse

def nada(x): pass

def detectar_color(ruta):
    # Cargar imagen
    img = cv2.imread(ruta)
    img = img[100:, :]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.namedWindow("Calibrador")
    cv2.createTrackbar("L-H", "Calibrador", 0, 180, nada)
    cv2.createTrackbar("L-S", "Calibrador", 0, 255, nada)
    cv2.createTrackbar("L-V", "Calibrador", 0, 255, nada)
    cv2.createTrackbar("U-H", "Calibrador", 180, 180, nada)
    cv2.createTrackbar("U-S", "Calibrador", 255, 255, nada)
    cv2.createTrackbar("U-V", "Calibrador", 255, 255, nada)

    while True:
        lh = cv2.getTrackbarPos("L-H", "Calibrador")
        ls = cv2.getTrackbarPos("L-S", "Calibrador")
        lv = cv2.getTrackbarPos("L-V", "Calibrador")
        uh = cv2.getTrackbarPos("U-H", "Calibrador")
        us = cv2.getTrackbarPos("U-S", "Calibrador")
        uv = cv2.getTrackbarPos("U-V", "Calibrador")
        
        mask = cv2.inRange(hsv, np.array([lh, ls, lv]), np.array([uh, us, uv]))
        
        cv2.imshow("Calibrador", mask)
        if cv2.waitKey(1) == 27: break 

    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script para calibrar parametros de mascara hsv"
    )

    # Definimos el argumento con doble guión (--ruta) tal como lo tenías
    parser.add_argument("--ruta", type=str, required=True, 
                        help="Ruta de la imagen a probar")
    
    args = parser.parse_args()

    detectar_color(ruta=args.ruta)