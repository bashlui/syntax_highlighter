#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para el resaltado de código Python
Este script automatiza el proceso de:
1. Ejecutar el analizador léxico en Racket
2. Generar el HTML con resaltado de sintaxis
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def ejecutar_racket(archivo_python, archivo_csv):
    """Ejecuta el analizador léxico en Racket"""
    print(f"Analizando {archivo_python} con Racket...")
    try:
        # Verificar que el archivo Python existe
        if not os.path.exists(archivo_python):
            print(f"Error: No se encontró el archivo {archivo_python}")
            return False
        
        # Verificar que el analizador léxico existe
        if not os.path.exists("analizador-lexico.rkt"):
            print("Error: No se encontró el archivo analizador-lexico.rkt")
            return False
        
        # Ejecutar Racket
        resultado = subprocess.run(
            ["racket", "analizador-lexico.rkt"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(resultado.stdout)
        
        # Verificar que se generó el archivo CSV
        if not os.path.exists(archivo_csv):
            print(f"Error: No se generó el archivo {archivo_csv}")
            return False
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Racket: {e}")
        print(f"Salida de error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def generar_html(archivo_csv, archivo_html):
    """Genera el HTML con resaltado de sintaxis"""
    print(f"Generando HTML a partir de {archivo_csv}...")
    try:
        # Verificar que el script generador existe
        if not os.path.exists("generar_html.py"):
            print("Error: No se encontró el archivo generar_html.py")
            return False
        
        # Ejecutar el script generador
        resultado = subprocess.run(
            ["python", "generar_html.py", archivo_csv, archivo_html],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(resultado.stdout)
        
        # Verificar que se generó el archivo HTML
        if not os.path.exists(archivo_html):
            print(f"Error: No se generó el archivo {archivo_html}")
            return False
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al generar HTML: {e}")
        print(f"Salida de error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def abrir_navegador(archivo_html):
    """Abre el archivo HTML en el navegador por defecto"""
    print(f"Abriendo {archivo_html} en el navegador...")
    try:
        # Obtener la ruta absoluta al archivo HTML
        ruta_absoluta = os.path.abspath(archivo_html)
        
        # Abrir el navegador
        webbrowser.open(f"file://{ruta_absoluta}")
        return True
    except Exception as e:
        print(f"Error al abrir el navegador: {e}")
        return False

def main():
    """Función principal"""
    # Configuración por defecto
    archivo_python = "prueba.py"
    archivo_csv = "tokens.csv"
    archivo_html = "resaltado_python.html"
    
    # Procesar argumentos
    if len(sys.argv) > 1:
        archivo_python = sys.argv[1]
    
    if len(sys.argv) > 2:
        archivo_html = sys.argv[2]
    
    # Modificar el archivo analizador-lexico.rkt para usar el archivo Python especificado
    try:
        with open("analizador-lexico.rkt", "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Reemplazar la línea de ejecución
        contenido_modificado = contenido.replace(
            '(main "prueba.py" "tokens.csv")',
            f'(main "{archivo_python}" "{archivo_csv}")'
        )
        
        with open("analizador-lexico.rkt", "w", encoding="utf-8") as f:
            f.write(contenido_modificado)
    except Exception as e:
        print(f"Error al modificar analizador-lexico.rkt: {e}")
        return 1
    
    # Ejecutar el proceso completo
    if ejecutar_racket(archivo_python, archivo_csv):
        if generar_html(archivo_csv, archivo_html):
            abrir_navegador(archivo_html)
            print("\n¡Proceso completado con éxito!")
            print(f"El archivo HTML se ha generado en: {archivo_html}")
            return 0
    
    print("\nEl proceso no se completó correctamente.")
    return 1

if __name__ == "__main__":
    sys.exit(main()) 