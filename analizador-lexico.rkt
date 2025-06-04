#lang racket

;; Analizador léxico para Python implementado en Racket funcional
;; Este programa identifica tokens de Python y los guarda en un archivo CSV

;; Definición de categorías léxicas con sus expresiones regulares
(define tokens
  `(
    ;; Cadenas triples (tienen prioridad sobre las cadenas simples)
    (STRING . ,(regexp "^(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?''')"))
    
    ;; Comentarios (solo hasta el final de la línea)
    (COMMENT . ,(regexp "^#[^\n]*"))
    
    ;; Cadenas simples y dobles
    (STRING . ,(regexp "^(\"[^\"\\n]*\"|'[^'\\n]*')"))
    
    ;; Números (enteros, flotantes, hexadecimales, binarios, octales, notación científica)
    (NUMBER . ,(regexp "^(0[xX][0-9a-fA-F]+|0[bB][01]+|0[oO][0-7]+|\\d+\\.\\d+|\\d+\\.|\\.\\d+|\\d+)([eE][+-]?\\d+)?"))
    
    ;; Palabras reservadas de Python (tienen prioridad sobre identificadores)
    (KEYWORD . ,(regexp "^(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\\b"))
    
    ;; Decoradores
    (DECORATOR . ,(regexp "^@[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Operadores
    (OPERATOR . ,(regexp "^(\\+\\+|\\-\\-|\\*\\*|//|==|!=|<=|>=|<>|<<|>>|\\+=|\\-=|\\*=|/=|%=|\\*\\*=|//=|&=|\\|=|\\^=|>>=|<<=|\\+|\\-|\\*|/|%|\\^|&|\\||~|<|>|=)"))
    
    ;; Delimitadores
    (DELIMITER . ,(regexp "^[()\\[\\]{},.:;@]"))
    
    ;; Identificadores (nombres de variables, funciones, etc.)
    (IDENTIFIER . ,(regexp "^[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Espacios en blanco (espacios, tabulaciones)
    (WHITESPACE . ,(regexp "^[ \t]+"))
    
    ;; Saltos de línea
    (NEWLINE . ,(regexp "^\n"))))

;; Función para encontrar el primer token que coincide con el input
(define (match-token input)
  (define (try-match token-list)
    (cond
      [(null? token-list) #f]
      [else
       (let* ([cat (car token-list)]
              [regex (cdr cat)]
              [match (regexp-match regex input)])
         (if match
             (cons (car cat) (car match))
             (try-match (cdr token-list))))]))
  (try-match tokens))

;; Función para tokenizar una cadena de entrada
(define (tokenize input)
  (define (loop pos acc)
    (if (>= pos (string-length input))
        (reverse acc)
        (let ([result (match-token (substring input pos))])
          (if result
              (let ([token (car result)]
                    [lexeme (cdr result)])
                (loop (+ pos (string-length lexeme)) (cons (list token lexeme) acc)))
              (let ([char (substring input pos (+ pos 1))])
                (loop (+ pos 1) (cons (list 'UNKNOWN char) acc)))))))
  (loop 0 '()))

;; Función para guardar tokens en un archivo CSV
(define (save-tokens-csv tokens filename)
  (call-with-output-file filename
    (lambda (out)
      (for-each
       (lambda (tok)
         (let* ([tipo (symbol->string (car tok))]
                [lexema (cadr tok)]
                [lexema-escaped (string-replace lexema "\"" "\"\"")])
           (fprintf out "\"~a\",\"~a\"\n" tipo lexema-escaped)))
       tokens))
    #:exists 'replace))

;; Función principal
(define (main input-path output-csv-path)
  (define content (file->string input-path))
  (define tokens-list (tokenize content))
  (save-tokens-csv tokens-list output-csv-path)
  (printf "Tokens guardados en: ~a\n" output-csv-path)
  (printf "Total de tokens identificados: ~a\n" (length tokens-list)))

;; Ejecución del programa
(main "ejemplo_completo.py" "tokens.csv")
