#lang racket

;; Analizador léxico para Python implementado en Racket funcional puro
;; Este programa analiza un archivo de código Python y genera un archivo CSV con los tokens identificados

;; Importar bibliotecas necesarias
(require racket/string)
(require racket/match)
(require racket/port)

;; Lista de palabras clave de Python
(define python-keywords
  '("and" "as" "assert" "async" "await" "break" "class" "continue" "def" "del"
    "elif" "else" "except" "False" "finally" "for" "from" "global" "if" "import"
    "in" "is" "lambda" "None" "nonlocal" "not" "or" "pass" "raise" "return"
    "True" "try" "while" "with" "yield"))

;; Crear la expresión regular para las palabras clave
(define keyword-regex
  (regexp (string-append "^\\b(" (string-join python-keywords "|") ")\\b")))

;; Definición de categorías léxicas con sus expresiones regulares
;; El orden es importante: de más específico a más general
(define token-patterns
  `(
    ;; Comentarios (solo hasta el final de la línea)
    ("COMMENT" . ,(regexp "^#[^\n]*"))
    
    ;; Cadenas triples (tienen prioridad sobre las cadenas simples)
    ("STRING_TRIPLE" . ,(regexp "^(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?''')"))
    
    ;; F-strings (manejan caracteres escapados)
    ("STRING_F" . ,(regexp "^[fF]('(\\\\.|[^'\\\\])*'|\"(\\\\.|[^\"\\\\])*\")"))
    
    ;; Cadenas simples y dobles (manejan caracteres escapados)
    ("STRING" . ,(regexp "^('(\\\\.|[^'\\\\])*'|\"(\\\\.|[^\"\\\\])*\")"))
    
    ;; Palabras reservadas de Python (tienen prioridad sobre identificadores)
    ("KEYWORD" . ,keyword-regex)
    
    ;; Números (enteros, flotantes, hexadecimales, binarios, octales, notación científica)
    ("NUMBER" . ,(regexp "^\\b(0[xX][0-9a-fA-F]+|0[bB][01]+|0[oO][0-7]+|\\d+\\.\\d*|\\.\\d+|\\d+)([eE][+-]?\\d+)?\\b"))
    
    ;; Decoradores
    ("DECORATOR" . ,(regexp "^@[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Operadores
    ("OPERATOR" . ,(regexp "^(\\*\\*=|//=|\\+=|-=|\\*=|/=|%=|&=|\\|=|\\^=|>>=|<<=|\\*\\*|//|==|!=|<=|>=|<>|<<|>>|\\+|-|\\*|/|%|\\^|&|\\||~|<|>|=)"))
    
    ;; Delimitadores
    ("DELIMITER" . ,(regexp "^[()\\[\\]{},.:;@]"))
    
    ;; Identificadores (nombres de variables, funciones, etc.)
    ("IDENTIFIER" . ,(regexp "^[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Espacios en blanco (espacios, tabulaciones)
    ("WHITESPACE" . ,(regexp "^[ \t]+"))
    
    ;; Saltos de línea
    ("NEWLINE" . ,(regexp "^\n"))))

;; Función para encontrar el token que coincide con el inicio del texto
(define (find-first-match text)
  (define (find-match patterns)
    (if (null? patterns)
        #f
        (let* ([pattern-pair (car patterns)]
               [category (car pattern-pair)]
               [regex (cdr pattern-pair)]
               [match (regexp-match regex text)])
          (if match
              (cons category (car match))
              (find-match (cdr patterns))))))
  (find-match token-patterns))

;; Función para tokenizar una cadena de texto
(define (tokenize-string text)
  (let loop ([remaining-text text]
             [tokens '()])
    (cond
      [(string=? remaining-text "") (reverse tokens)]
      [else
       (let ([match (find-first-match remaining-text)])
         (if match
             (let ([category (car match)]
                   [lexeme (cdr match)]
                   [new-text (substring remaining-text (string-length (cdr match)))])
               (loop new-text (cons (list category lexeme) tokens)))
             ;; Si no hay coincidencia, considerar el carácter como desconocido
             (let ([unknown-char (substring remaining-text 0 1)]
                   [new-text (substring remaining-text 1)])
               (loop new-text (cons (list "UNKNOWN" unknown-char) tokens)))))])))

;; Función para leer un archivo y devolver su contenido como una cadena
(define (read-file-to-string file-path)
  (with-input-from-file file-path
    (lambda ()
      (port->string (current-input-port)))))

;; Función para escapar comillas dobles en una cadena para CSV
(define (escape-csv-string str)
  (string-replace (string-replace str "\"" "\"\"") "\n" "\\n"))

;; Función para escribir tokens en un archivo CSV
(define (write-tokens-to-csv tokens output-file)
  (with-output-to-file output-file
    #:exists 'replace
    (lambda ()
      (for-each
       (lambda (token)
         (let ([category (first token)]
               [lexeme (second token)])
           (printf "\"~a\",\"~a\"\n" category (escape-csv-string lexeme))))
       tokens))))

;; Función principal
(define (main)
  (define args (current-command-line-arguments))
  (define input-file (if (> (vector-length args) 0)
                        (vector-ref args 0)
                        "ejemplo.py"))
  (define output-file (if (> (vector-length args) 1)
                         (vector-ref args 1)
                         "tokens.csv"))
  
  (printf "Analizando archivo: ~a\n" input-file)
  (let* ([code (read-file-to-string input-file)]
         [tokens (tokenize-string code)])
    (write-tokens-to-csv tokens output-file)
    (printf "Análisis completado. Se encontraron ~a tokens.\n" (length tokens))
    (printf "Resultados guardados en: ~a\n" output-file)))

;; Ejecutar la función principal
(main)