# Analizador Léxico para Python

Este proyecto implementa un analizador léxico para Python utilizando Racket (para el análisis léxico) y Python (para la generación del HTML con resaltado de sintaxis).

## Categorías Léxicas de Python

El analizador reconoce las siguientes categorías léxicas:

- **KEYWORD**: Palabras reservadas de Python (if, else, for, while, etc.)
- **IDENTIFIER**: Identificadores (nombres de variables, funciones, etc.)
- **NUMBER**: Números (enteros, flotantes, hexadecimales, etc.)
- **STRING**: Cadenas de texto (simples, dobles)
- **STRING_TRIPLE**: Cadenas de texto triples (""" o ''')
- **STRING_F**: Cadenas f-string
- **COMMENT**: Comentarios
- **OPERATOR**: Operadores (+, -, *, /, etc.)
- **DELIMITER**: Delimitadores (paréntesis, corchetes, etc.)
- **DECORATOR**: Decoradores (@property, @staticmethod, etc.)
- **WHITESPACE**: Espacios en blanco
- **NEWLINE**: Saltos de línea

## Archivo de Ejemplo

El archivo `ejemplo.py` incluye ejemplos de todos los tipos de tokens que el analizador puede reconocer:

- Palabras clave (if, else, for, while, try, except, etc.)
- Diferentes tipos de identificadores (snake_case, CamelCase, etc.)
- Números (enteros, flotantes, hexadecimales, binarios, octales, complejos)
- Cadenas de texto (simples, dobles, triples, f-strings)
- Operadores aritméticos, de comparación, lógicos y de bits
- Delimitadores y otros elementos sintácticos

Este archivo sirve como prueba exhaustiva para verificar el correcto funcionamiento del analizador léxico.

## Expresiones Regulares

Cada categoría léxica se define mediante expresiones regulares:

```racket
;; Palabras reservadas
"^\\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\\b"

;; Cadenas triples
"^(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?''')"

;; Comentarios
"^#.*"

;; F-strings
"^[fF](\"[^\"\\n]*\"|'[^'\\n]*')"

;; Cadenas simples y dobles
"^(\"[^\"\\n]*\"|'[^'\\n]*')"

;; Números
"^\\b(0[xX][0-9a-fA-F]+|0[bB][01]+|0[oO][0-7]+|\\d+\\.\\d*|\\.\\d+|\\d+)([eE][+-]?\\d+)?\\b"

;; Decoradores
"^@[a-zA-Z_][a-zA-Z0-9_]*"

;; Operadores
"^(\\*\\*=|//=|\\+=|-=|\\*=|/=|%=|&=|\\|=|\\^=|>>=|<<=|\\*\\*|//|==|!=|<=|>=|<>|<<|>>|\\+|-|\\*|/|%|\\^|&|\\||~|<|>|=)"

;; Delimitadores
"^[()\\[\\]{},.:;@]"

;; Identificadores
"^[a-zA-Z_][a-zA-Z0-9_]*"

;; Espacios en blanco
"^[ \t]+"

;; Saltos de línea
"^\n"
```

## Requisitos

- Racket (versión 7.0 o superior)
- Python 3.6 o superior

## Instalación

1. Instala Racket desde [racket-lang.org](https://racket-lang.org/download/)
2. Asegúrate de tener Python 3.6 o superior instalado
3. Clona o descarga este repositorio

Para más detalles sobre la instalación, consulta el archivo `INSTALACION.md`.

## Uso

La forma más sencilla de usar el programa es mediante el script `generar_html.py`:

```bash
python generar_html.py [archivo_csv] [archivo_html_salida]
```

Para generar el archivo CSV de tokens:

```bash
racket analizador-lexico.rkt [archivo_python] [archivo_csv_salida]
```

### Ejemplo completo:

```bash
racket analizador-lexico.rkt ejemplo.py tokens.csv
python generar_html.py tokens.csv resaltado_python.html
```

## Estructura del Proyecto

- `analizador-lexico.rkt`: Implementación del analizador léxico en Racket funcional puro
- `generar_html.py`: Script Python para generar HTML con resaltado de sintaxis
- `ejemplo.py`: Archivo de ejemplo con código Python que muestra todos los tipos de tokens
- `syntax_highlighter.css`: Estilos CSS para el resaltado de sintaxis
- `tokens.csv`: Archivo generado con los tokens identificados
- `resaltado_python.html`: Archivo HTML generado con el código resaltado
- `verificador.py`: Script para verificar la correcta tokenización
- `automatas.md`: Documentación sobre los autómatas utilizados
- `INSTALACION.md`: Guía detallada de instalación
- `README.md`: Este archivo

## Personalización

### Modificar los Estilos

Puedes personalizar los estilos de resaltado modificando el archivo `syntax_highlighter.css`.

### Añadir Nuevas Categorías Léxicas

Para añadir nuevas categorías léxicas:

1. Añade la expresión regular correspondiente en `analizador-lexico.rkt`
2. Añade el estilo CSS para la nueva categoría en `syntax_highlighter.css`

## Implementación

El programa combina programación funcional en Racket con Python:

1. **Racket** (funcional puro): Implementa el analizador léxico que tokeniza el código fuente
2. **Python**: Procesa los tokens y genera un HTML con resaltado de sintaxis

## Licencia

Este proyecto es de código abierto y se distribuye bajo la licencia MIT. 