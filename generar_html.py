#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de HTML para resaltado de sintaxis de Python
Este script lee un archivo CSV con tokens generados por el analizador léxico en Racket
y genera un archivo HTML con resaltado de sintaxis.
"""

import os
import sys
import csv
import html
import re
from datetime import datetime

# Lista de funciones "built-in" de Python
PYTHON_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
    'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict',
    'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id',
    'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals',
    'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
    'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set',
    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple',
    'type', 'vars', 'zip'
}

def leer_tokens_csv(archivo_csv):
    """Lee los tokens desde un archivo CSV con formato simplificado"""
    tokens = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            # Leer con DictReader para manejar encabezados
            lector_csv = csv.DictReader(f)
            for fila in lector_csv:
                # Adaptarse al nuevo formato CSV
                if 'tipo' in fila and 'lexema' in fila:
                    tipo = fila['tipo']
                    lexema = fila['lexema'].replace('\\n', '\n')
                    tokens.append((tipo, lexema))
                # Compatibilidad con formato anterior
                elif 'Category' in fila and 'Lexeme' in fila:
                    tipo = fila['Category']
                    lexema = fila['Lexeme'].replace('\\n', '\n')
                    tokens.append((tipo, lexema))
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        sys.exit(1)
    return tokens

def post_process_tokens(tokens):
    """Re-clasifica identificadores basados en el contexto."""
    processed_tokens = list(tokens)
    
    # Primera pasada: identificar funciones definidas en el código
    defined_functions = set()
    for i in range(len(processed_tokens)):
        token_type, lexeme = processed_tokens[i]
        if token_type == 'IDENTIFIER':
            # Verificar si es una definición de función
            prev_token_index = i - 1
            while prev_token_index >= 0 and processed_tokens[prev_token_index][0] == 'WHITESPACE':
                prev_token_index -= 1
                
            if prev_token_index >= 0 and processed_tokens[prev_token_index] == ('KEYWORD', 'def'):
                defined_functions.add(lexeme)
    
    # Segunda pasada: procesar tokens
    for i in range(len(processed_tokens)):
        token_type, lexeme = processed_tokens[i]

        if token_type == 'IDENTIFIER':
            # Reclasificar funciones "built-in"
            if lexeme in PYTHON_BUILTINS:
                # Comprobar si es una llamada a función
                next_token_index = i + 1
                # Saltar espacios en blanco
                while next_token_index < len(processed_tokens) and processed_tokens[next_token_index][0] == 'WHITESPACE':
                    next_token_index += 1
                
                if next_token_index < len(processed_tokens) and processed_tokens[next_token_index][1] == '(':
                    processed_tokens[i] = ('BUILTIN_FUNCTION', lexeme)
                continue
                
            # Verificar si es una llamada a una función definida en el código
            if lexeme in defined_functions:
                next_token_index = i + 1
                # Saltar espacios en blanco
                while next_token_index < len(processed_tokens) and processed_tokens[next_token_index][0] == 'WHITESPACE':
                    next_token_index += 1
                
                if next_token_index < len(processed_tokens) and processed_tokens[next_token_index][1] == '(':
                    processed_tokens[i] = ('FUNCTION_CALL', lexeme)
                continue

            # Reclasificar nombres de clase y función
            prev_token_index = i - 1
            # Saltar espacios en blanco
            while prev_token_index >= 0 and processed_tokens[prev_token_index][0] == 'WHITESPACE':
                prev_token_index -= 1

            if prev_token_index >= 0:
                prev_token_type, prev_lexeme = processed_tokens[prev_token_index]
                if prev_token_type == 'KEYWORD' and prev_lexeme in ['class', 'def']:
                    new_type = 'CLASS_NAME' if prev_lexeme == 'class' else 'FUNCTION_NAME'
                    processed_tokens[i] = (new_type, lexeme)

    # Tercera pasada: identificar parámetros de funciones
    i = 0
    while i < len(processed_tokens):
        token_type, lexeme = processed_tokens[i]
        
        if token_type == 'FUNCTION_NAME':
            # Buscar paréntesis de apertura
            paren_index = i + 1
            while paren_index < len(processed_tokens) and processed_tokens[paren_index][1] != '(':
                paren_index += 1
                
            if paren_index < len(processed_tokens):
                # Encontrado el paréntesis, ahora buscar parámetros
                param_index = paren_index + 1
                paren_level = 1
                
                while param_index < len(processed_tokens) and paren_level > 0:
                    param_type, param_lexeme = processed_tokens[param_index]
                    
                    if param_lexeme == '(':
                        paren_level += 1
                    elif param_lexeme == ')':
                        paren_level -= 1
                    elif param_type == 'IDENTIFIER' and paren_level == 1:
                        # Es un parámetro de función
                        if param_lexeme == 'self':
                            processed_tokens[param_index] = ('SELF_PARAM', param_lexeme)
                        else:
                            processed_tokens[param_index] = ('PARAMETER', param_lexeme)
                    
                    param_index += 1
        
        i += 1
    
    return processed_tokens

def generar_html(tokens, archivo_salida, titulo="Resaltado de Sintaxis Python", usar_css_externo=True):
    """Genera un archivo HTML con los tokens resaltados"""
    # Aplicar post-procesamiento
    tokens_procesados = post_process_tokens(tokens)
    
    # Contar tokens por tipo
    conteo_tokens = {}
    for tipo, _ in tokens_procesados:
        conteo_tokens[tipo] = conteo_tokens.get(tipo, 0) + 1
    
    # Generar HTML
    html_content = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n"
    html_content += "    <meta charset=\"UTF-8\">\n"
    html_content += "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
    html_content += f"    <title>{titulo}</title>\n"
    
    # Incluir CSS
    if usar_css_externo:
        html_content += "    <link rel=\"stylesheet\" href=\"syntax_highlighter.css\">\n"
    else:
        html_content += "    <style>\n"
        html_content += "        body {\n"
        html_content += "            font-family: 'Courier New', monospace;\n"
        html_content += "            background: #f8f8f8;\n"
        html_content += "            padding: 20px;\n"
        html_content += "            line-height: 1.6;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        h1 {\n"
        html_content += "            color: #333;\n"
        html_content += "            text-align: center;\n"
        html_content += "            margin-bottom: 30px;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .container {\n"
        html_content += "            max-width: 1200px;\n"
        html_content += "            margin: 0 auto;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .code-container {\n"
        html_content += "            background: #272822;\n"
        html_content += "            padding: 20px;\n"
        html_content += "            border-radius: 8px;\n"
        html_content += "            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);\n"
        html_content += "            overflow: auto;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        pre {\n"
        html_content += "            margin: 0;\n"
        html_content += "            padding: 0;\n"
        html_content += "            background: #272822;\n"
        html_content += "            color: #f8f8f2;\n"
        html_content += "            white-space: pre-wrap;\n"
        html_content += "            tab-size: 4;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .stats {\n"
        html_content += "            margin-top: 30px;\n"
        html_content += "            background: #fff;\n"
        html_content += "            padding: 20px;\n"
        html_content += "            border-radius: 8px;\n"
        html_content += "            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .stats h2 {\n"
        html_content += "            color: #333;\n"
        html_content += "            margin-top: 0;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .stats-grid {\n"
        html_content += "            display: grid;\n"
        html_content += "            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));\n"
        html_content += "            gap: 15px;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .stat-item {\n"
        html_content += "            background: #f1f1f1;\n"
        html_content += "            padding: 10px;\n"
        html_content += "            border-radius: 5px;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        .footer {\n"
        html_content += "            margin-top: 30px;\n"
        html_content += "            text-align: center;\n"
        html_content += "            color: #777;\n"
        html_content += "        }\n"
        html_content += "        \n"
        html_content += "        /* Estilos para los tokens */\n"
        html_content += "        .KEYWORD { color: #66d9ef; font-weight: bold; }\n"
        html_content += "        .IDENTIFIER { color: #f8f8f2; }\n"
        html_content += "        .NUMBER { color: #ae81ff; }\n"
        html_content += "        .STRING, .STRING_TRIPLE, .STRING_F { color: #e6db74; }\n"
        html_content += "        .COMMENT { color: #75715e; font-style: italic; }\n"
        html_content += "        .OPERATOR { color: #f92672; }\n"
        html_content += "        .DELIMITER { color: #a6e22e; }\n"
        html_content += "        .DECORATOR { color: #a1efe4; font-weight: bold; }\n"
        html_content += "        .UNKNOWN { color: #fd971f; }\n"
        html_content += "    </style>\n"
    
    html_content += "</head>\n<body>\n"
    html_content += "    <div class=\"container\">\n"
    html_content += f"        <h1>{titulo}</h1>\n"
    html_content += "        \n"
    html_content += "        <div class=\"code-container\">\n"
    html_content += "            <pre>"
    
    # Generar HTML para cada token
    for tipo, lexema in tokens_procesados:
        if tipo == "WHITESPACE":
            html_content += html.escape(lexema).replace(' ', '&nbsp;')
        elif tipo == "NEWLINE":
            html_content += "<br>"
        else:
            html_content += f'<span class="{tipo}">{html.escape(lexema)}</span>'
    
    html_content += "</pre>\n"
    html_content += "        </div>\n"
    html_content += "        \n"
    html_content += "        <div class=\"stats\">\n"
    html_content += "            <h2>Estadísticas</h2>\n"
    html_content += "            <div class=\"stats-grid\">\n"
    html_content += f"                <div class=\"stat-item\">\n"
    html_content += f"                    <strong>Total de tokens:</strong> {len(tokens_procesados)}\n"
    html_content += f"                </div>\n"
    
    # Agregar estadísticas por tipo de token
    for tipo, cantidad in sorted(conteo_tokens.items()):
        html_content += f"                <div class=\"stat-item\"><strong>{tipo}:</strong> {cantidad}</div>\n"
    
    html_content += "            </div>\n"
    html_content += "        </div>\n"
    html_content += "        \n"
    html_content += "        <div class=\"footer\">\n"
    html_content += f"            <p>Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
    html_content += "        </div>\n"
    html_content += "    </div>\n"
    html_content += "</body>\n</html>"
    
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
    if len(sys.argv) < 2:
        print("Uso: python generar_html.py <archivo_csv> [<archivo_html_salida>]")
        sys.exit(1)
    
    archivo_csv = sys.argv[1]
    archivo_html = sys.argv[2] if len(sys.argv) > 2 else "resaltado_python.html"
    
    # Leer tokens
    tokens = leer_tokens_csv(archivo_csv)
    
    # Generar HTML
    generar_html(tokens, archivo_html)

if __name__ == "__main__":
    main() 