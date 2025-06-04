#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de HTML para resaltado de sintaxis Python
Este script lee los tokens generados por el analizador léxico en Racket
y crea un archivo HTML con resaltado de sintaxis
"""

import csv
import os
import sys
import html
from datetime import datetime

def leer_tokens(archivo_csv):
    """Lee los tokens desde un archivo CSV"""
    tokens = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            lector = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
            for fila in lector:
                if len(fila) == 2:
                    tipo, lexema = fila
                    tokens.append((tipo, lexema))
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        sys.exit(1)
    return tokens

def token_a_html(token):
    """Convierte un token en su representación HTML"""
    tipo, lexema = token
    
    # Escapar caracteres especiales HTML
    lexema_escapado = html.escape(lexema)
    
    # Reemplazar saltos de línea por <br>
    lexema_escapado = lexema_escapado.replace('\n', '<br>')
    
    if tipo == "WHITESPACE":
        return lexema_escapado
    else:
        return f'<span class="{tipo}">{lexema_escapado}</span>'

def generar_html(tokens, archivo_salida, titulo="Resaltado de Sintaxis Python"):
    """Genera un archivo HTML con los tokens resaltados"""
    # Contar tokens por tipo
    conteo_tokens = {}
    for tipo, _ in tokens:
        if tipo in conteo_tokens:
            conteo_tokens[tipo] += 1
        else:
            conteo_tokens[tipo] = 1
    
    # Generar HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #f8f8f8;
            padding: 20px;
            line-height: 1.6;
        }}
        
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .code-container {{
            background: #272822;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: auto;
        }}
        
        pre {{
            margin: 0;
            padding: 0;
            background: #272822;
            color: #f8f8f2;
            white-space: pre-wrap;
        }}
        
        .stats {{
            margin-top: 30px;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        
        .stats h2 {{
            color: #333;
            margin-top: 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .stat-item {{
            background: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
        }}
        
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #777;
        }}
        
        /* Estilos para los tokens */
        .KEYWORD {{ color: #66d9ef; font-weight: bold; }}
        .IDENTIFIER {{ color: #f8f8f2; }}
        .NUMBER {{ color: #ae81ff; }}
        .STRING {{ color: #e6db74; }}
        .COMMENT {{ color: #75715e; font-style: italic; }}
        .OPERATOR {{ color: #f92672; }}
        .DELIMITER {{ color: #a6e22e; }}
        .DECORATOR {{ color: #a1efe4; font-weight: bold; }}
        .UNKNOWN {{ color: #fd971f; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{titulo}</h1>
        
        <div class="code-container">
            <pre>{"".join(token_a_html(token) for token in tokens)}</pre>
        </div>
        
        <div class="stats">
            <h2>Estadísticas</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <strong>Total de tokens:</strong> {len(tokens)}
                </div>
                {"".join(f'<div class="stat-item"><strong>{tipo}:</strong> {cantidad}</div>' for tipo, cantidad in conteo_tokens.items())}
            </div>
        </div>
        
        <div class="footer">
            <p>Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Guardar el archivo HTML
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Archivo HTML generado: {archivo_salida}")
    except Exception as e:
        print(f"Error al escribir el archivo HTML: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    # Verificar argumentos
    if len(sys.argv) > 1:
        archivo_csv = sys.argv[1]
    else:
        archivo_csv = "tokens.csv"
    
    if len(sys.argv) > 2:
        archivo_salida = sys.argv[2]
    else:
        archivo_salida = "resaltado_python.html"
    
    # Verificar que el archivo CSV existe
    if not os.path.exists(archivo_csv):
        print(f"Error: No se encontró el archivo {archivo_csv}")
        print("Primero debes ejecutar el analizador léxico con:")
        print("  racket analizador-lexico.rkt")
        sys.exit(1)
    
    # Leer tokens y generar HTML
    tokens = leer_tokens(archivo_csv)
    generar_html(tokens, archivo_salida)
    
    print(f"Se procesaron {len(tokens)} tokens")
    print(f"Puedes abrir {archivo_salida} en tu navegador para ver el resultado")

if __name__ == "__main__":
    main() 