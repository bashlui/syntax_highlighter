#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador para el analizador léxico
Este script abre el archivo HTML generado en el navegador por defecto
"""

import os
import sys
import webbrowser
from pathlib import Path

def main():
    """Función principal del verificador"""
    # Verificar si existe el archivo HTML
    html_file = "salida.html"
    if not os.path.exists(html_file):
        print(f"Error: No se encontró el archivo {html_file}")
        print("Primero debes ejecutar el analizador léxico con:")
        print("  racket analizador-lexico.rkt")
        return 1
    
    # Obtener la ruta absoluta al archivo HTML
    html_path = os.path.abspath(html_file)
    
    # Abrir el archivo en el navegador por defecto
    print(f"Abriendo {html_file} en el navegador...")
    webbrowser.open(f"file://{html_path}")
    print("Si el navegador no muestra los colores correctamente, intenta:")
    print("1. Abrir el archivo manualmente desde el navegador")
    print("2. Verificar que el archivo HTML se generó correctamente")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 