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
from datetime import datetime

def leer_tokens_csv(archivo_csv):
    """Lee los tokens desde un archivo CSV"""
    tokens = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            lector_csv = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
            for fila in lector_csv:
                if len(fila) >= 2:
                    tipo = fila[0]
                    lexema = fila[1].replace('\\n', '\n')
                    tokens.append((tipo, lexema))
                # Omitir filas vacías o malformadas en silencio
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        sys.exit(1)
    return tokens

def post_process_tokens(tokens):
    """Re-clasifica identificadores basados en el contexto (clases, funciones, parámetros)."""
    processed_tokens = list(tokens)  # Crear una copia mutable

    for i in range(len(processed_tokens) - 2):
        t_keyword = processed_tokens[i]
        t_space = processed_tokens[i+1]
        t_name = processed_tokens[i+2]

        # Patrón: KEYWORD('class'/'def') WHITESPACE IDENTIFIER
        if (t_keyword[0] == 'KEYWORD' and t_keyword[1] in ['class', 'def'] and
            t_space[0] == 'WHITESPACE' and
            t_name[0] == 'IDENTIFIER'):
            
            new_type = 'CLASS_NAME' if t_keyword[1] == 'class' else 'FUNCTION_NAME'
            processed_tokens[i+2] = (new_type, t_name[1])

            # Si es una función, buscar los parámetros
            if new_type == 'FUNCTION_NAME':
                paren_level = 0
                start_paren = -1
                end_paren = -1

                # Buscar el bloque de paréntesis (...)
                for j in range(i + 3, len(processed_tokens)):
                    if j >= len(processed_tokens): break
                    
                    lexeme = processed_tokens[j][1]
                    if lexeme == '(':
                        if paren_level == 0: start_paren = j
                        paren_level += 1
                    elif lexeme == ')':
                        paren_level -= 1
                        if paren_level == 0:
                            end_paren = j
                            break
                
                # Si se encuentra un bloque de paréntesis, clasificar los parámetros
                if start_paren != -1 and end_paren != -1:
                    for k in range(start_paren + 1, end_paren):
                        if processed_tokens[k][0] == 'IDENTIFIER':
                            param_lexeme = processed_tokens[k][1]
                            if param_lexeme == 'self':
                                processed_tokens[k] = ('SELF_PARAM', param_lexeme)
                            else:
                                processed_tokens[k] = ('PARAMETER', param_lexeme)

    return processed_tokens

def token_a_html(token):
    """Convierte un token en su representación HTML"""
    tipo, lexema = token
    lexema_escapado = html.escape(lexema).replace('\n', '<br>')
    
    if tipo == "WHITESPACE":
        return lexema_escapado.replace(' ', '&nbsp;')
    elif tipo == "NEWLINE":
        return "<br>"
    else:
        return f'<span class="{tipo}">{lexema_escapado}</span>'

def generar_html(tokens, archivo_salida, titulo="Resaltado de Sintaxis Python", usar_css_externo=True):
    """Genera un archivo HTML con los tokens resaltados"""
    # Contar tokens por tipo
    conteo_tokens = {}
    for tipo, _ in tokens:
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
    
    # Agregar tokens
    html_content += "".join(token_a_html(token) for token in tokens)
    
    html_content += "</pre>\n"
    html_content += "        </div>\n"
    html_content += "        \n"
    html_content += "        <div class=\"stats\">\n"
    html_content += "            <h2>Estadísticas</h2>\n"
    html_content += "            <div class=\"stats-grid\">\n"
    html_content += f"                <div class=\"stat-item\">\n"
    html_content += f"                    <strong>Total de tokens:</strong> {len(tokens)}\n"
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
        print(f"Uso: {sys.argv[0]} archivo_tokens.csv [archivo_salida.html]")
        sys.exit(1)
    
    archivo_csv = sys.argv[1]
    
    if len(sys.argv) > 2:
        archivo_salida = sys.argv[2]
    else:
        archivo_salida = "resaltado_python.html"
    
    # Verificar que el archivo CSV existe
    if not os.path.exists(archivo_csv):
        print(f"Error: No se encontró el archivo {archivo_csv}")
        sys.exit(1)
    
    # Leer tokens y generar HTML
    raw_tokens = leer_tokens_csv(archivo_csv)
    tokens = post_process_tokens(raw_tokens)
    generar_html(tokens, archivo_salida)
    
    print(f"Se procesaron {len(tokens)} tokens")
    print(f"Puedes abrir {archivo_salida} en tu navegador para ver el resultado")

if __name__ == "__main__":
    main() 