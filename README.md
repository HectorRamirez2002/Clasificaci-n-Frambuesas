# Detección y Clasificación de Frambuesas en Líneas de Chocolatería Automatizada

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-TensorFlow%20%7C%20PyTorch-orange.svg)
![IDE](https://img.shields.io/badge/IDE-VS%20Code-purple.svg)
![Metodología](https://img.shields.io/badge/Metodolog%C3%ADa-%C3%81gil%20%2F%20Scrum-green.svg)

## Descripción del Proyecto

Este proyecto aborda la automatización del control de calidad en la producción de **chocolatería fina e industrial**. El objetivo principal es desarrollar y evaluar una **Red Neuronal Convolucional (CNN)** para la clasificación binaria de frambuesas (*raspberries*) en tiempo real mientras avanzan por una cinta transportadora, justo antes de ingresar a la **cascada de bañado en chocolate**.

En este entorno de manufactura alimentaria, la detección temprana es crítica: encapsular una fruta defectuosa dentro de un bombón compromete la seguridad inocua del producto, genera gases de descomposición que rompen el templado del chocolate y arruina lotes completos de producción. 

El sistema inspecciona visualmente el flujo de fruta para clasificarlo en dos categorías:
* **Apta para Bañado (`Healthy`):** Frambuesas estructuralmente firmes, maduras y completamente limpias, capaces de resistir el peso y calor del chocolate fluido.
* **Rechazada (`Damaged / Rotten`):** Frambuesas que presentan aplastamiento, ablandamiento severo, o signos de putrefacción (como moho blanco o *Botrytis*), los cuales destruirían la calidad microbiológica y el sabor del producto final.

---

## Tecnologías y Entorno Local

Para garantizar la reproducibilidad y el trabajo colaborativo ágil dentro del equipo, se ha estandarizado el entorno de desarrollo directamente en local utilizando:
* **IDE:** Visual Studio Code (VS Code) + Extensión de Jupyter Notebooks (`.ipynb`).
* **Control de Versiones:** Git & GitHub.
* **Librerías Clave:** OpenCV (Preprocesamiento), Matplotlib (Visualización), NumPy (Álgebra lineal), junto con TensorFlow/Keras o PyTorch para el modelado de la CNN.

---

## Estructura del Proyecto y Sincronización de Datos

A diferencia de los flujos de almacenamiento locales tradicionales, **este proyecto utiliza GitHub como el almacenamiento centralizado de datos (Data Repository)**. Cada desarrollador mantiene una copia idéntica del dataset en local. Cualquier adición, depuración o filtrado de imágenes se gestiona mediante comandos Git (`push` / `pull`), asegurando que todo el equipo entrene la CNN con la misma versión de los datos.

La estructura del espacio de trabajo compartido es la siguiente:

```text
Proyecto: Clasificación de frambuesas/
├── README.md                # Documentación del proyecto
├── 01_data_processing.ipynb # Cuaderno de preprocesamiento y aumento de datos (en proceso)
├── 02_cnn_model.ipynb       # Cuaderno de arquitectura, entrenamiento y evaluación (en proceso)
└── dataset/                 # Dataset
    ├── train/
    │   ├── sana/            # Imágenes de entrenamiento - Frambuesas Aptas
    │   └── danada/          # Imágenes de entrenamiento - Frutas Rechazadas/Con Moho
    └── validation/
        ├── sana/            # Imágenes de validación - Frambuesas Aptas
        └── danada/          # Imágenes de validación - Frutas Rechazadas/Con Moho