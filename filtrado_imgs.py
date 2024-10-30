import os
import shutil
import random
from pathlib import Path

def mover_imagenes():
    """
    Mueve una imagen aleatoria de cada subcarpeta en 'images' 
    a una carpeta 'images_moved' manteniendo la estructura
    """
    carpeta_origen = "images"
    carpeta_destino = "images_moved"
    
    # Verificar que la carpeta de origen existe
    if not os.path.exists(carpeta_origen):
        print(f"Error: La carpeta {carpeta_origen} no existe")
        return
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"Creada carpeta de destino: {carpeta_destino}")
    
    # Contador para seguimiento
    carpetas_procesadas = 0
    imagenes_movidas = 0
    
    # Recorrer todas las subcarpetas en la carpeta de origen
    for ruta_actual, subcarpetas, archivos in os.walk(carpeta_origen):
        # Filtrar solo archivos de imagen
        imagenes = [f for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if imagenes:  # Si hay imágenes en la carpeta actual
            carpetas_procesadas += 1
            
            # Obtener la ruta relativa para mantener la estructura
            ruta_relativa = os.path.relpath(ruta_actual, carpeta_origen)
            
            # Crear la subcarpeta correspondiente en el destino
            carpeta_destino_actual = os.path.join(carpeta_destino, ruta_relativa)
            if not os.path.exists(carpeta_destino_actual):
                os.makedirs(carpeta_destino_actual)
            
            # Seleccionar una imagen aleatoria
            imagen_a_mover = random.choice(imagenes)
            
            # Rutas completas de origen y destino
            ruta_origen = os.path.join(ruta_actual, imagen_a_mover)
            ruta_destino = os.path.join(carpeta_destino_actual, imagen_a_mover)
            
            try:
                # Mover la imagen
                shutil.move(ruta_origen, ruta_destino)
                imagenes_movidas += 1
                print(f"✓ Movida: {imagen_a_mover}")
                print(f"  De: {ruta_actual}")
                print(f"  A: {carpeta_destino_actual}")
                print("-" * 50)
            except Exception as e:
                print(f"✗ Error al mover {imagen_a_mover}: {str(e)}")
    
    # Resumen final
    print("\nResumen:")
    print(f"Carpetas procesadas: {carpetas_procesadas}")
    print(f"Imágenes movidas: {imagenes_movidas}")

if __name__ == "__main__":
    mover_imagenes()


