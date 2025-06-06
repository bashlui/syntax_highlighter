#lang racket

;; Analizador léxico para Python implementado en Racket funcional puro
;; Este programa analiza un archivo de código Python y genera un archivo CSV con los tokens identificados

(require racket/string)
(require racket/match)
(require racket/port)

;; Función para leer el contenido de un archivo a una cadena
(define (read-file-to-string file-path)
  (with-input-from-file file-path
    (lambda ()
      (port->string (current-input-port)))))

;; Lista de palabras clave de Python para la re-clasificación
(define python-keywords
  (set "and" "as" "assert" "async" "await" "break" "class" "continue" "def" "del"
       "elif" "else" "except" "False" "finally" "for" "from" "global" "if" "import"
       "in" "is" "lambda" "None" "nonlocal" "not" "or" "pass" "raise" "return"
       "True" "try" "while" "with" "yield"))

;; Definición de categorías léxicas con sus expresiones regulares
(define token-patterns
  `(
    ;; Comentarios
    ("COMMENT" . ,(pregexp "#.*"))
    
    ;; Cadenas
    ("STRING_TRIPLE" . ,(pregexp "(?s:\"\"\".*?\"\"\"|'''.*?''')"))
    ("STRING_F" . ,(pregexp "[fF](['\"].*?['\"])"))
    ("STRING" . ,(pregexp "(['\"].*?['\"])"))
    
    ;; Números
    ("NUMBER_FLOAT" . ,(pregexp "\\d+\\.\\d*([eE][+-]?\\d+)?"))
    ("NUMBER_FLOAT" . ,(pregexp "\\.\\d+([eE][+-]?\\d+)?"))
    ("NUMBER_HEX" . ,(pregexp "0[xX][0-9a-fA-F]+"))
    ("NUMBER_BIN" . ,(pregexp "0[bB][01]+"))
    ("NUMBER_OCT" . ,(pregexp "0[oO][0-7]+"))
    ("NUMBER_INT" . ,(pregexp "\\d+"))
    
    ;; Operadores
    ("OPERATOR" . ,(pregexp "\\*\\*=|//=|\\+=|-=|\\*=|/=|%=|&=|\\|=|\\^=|>>=|<<=|\\*\\*|//|==|!=|<=|>=|<>|<<|>>|\\+|-|\\*|/|%|\\^|&|\\||~|<|>|=|@"))
    
    ;; Delimitadores
    ("DELIMITER" . ,(pregexp "[][(){},:;.@?]"))
    
    ;; Decoradores
    ("DECORATOR" . ,(pregexp "@[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Identificadores
    ("IDENTIFIER" . ,(pregexp "[a-zA-Z_][a-zA-Z0-9_]*"))
    
    ;; Espacios
    ("WHITESPACE" . ,(pregexp "[ \t]+"))
    ("NEWLINE" . ,(pregexp "\n"))
    ))

;; Función auxiliar para contar caracteres
(define (count-char str char)
  (length (regexp-match* (regexp (string #\\ char)) str)))

;; Función para encontrar tokens
(define (find-first-match text)
  (define (find-match patterns)
    (if (null? patterns)
        #f
        (let* ([pattern-pair (car patterns)]
               [category (car pattern-pair)]
               [regex (cdr pattern-pair)]
               [match (regexp-match-positions regex text)])
          (if match
              (let ([start (caar match)]
                    [end (cdar match)])
                (if (zero? start)
                    (cons category (substring text start end))
                    (find-match (cdr patterns))))
              (find-match (cdr patterns))))))
  (find-match token-patterns))

;; Función principal de tokenización
(define (tokenize-string text)
  (let loop ([remaining-text text]
             [tokens '()]
             [line 1]
             [col 1])
    (cond
      [(string=? remaining-text "") (reverse tokens)]
      [else
       (let ([match (find-first-match remaining-text)])
         (if match
             (let* ([category (car match)]
                    [lexeme (cdr match)]
                    [lexeme-length (string-length lexeme)]
                    [new-text (substring remaining-text lexeme-length)]
                    [final-category (cond
                                     [(and (string=? category "IDENTIFIER")
                                           (set-member? python-keywords (string-downcase lexeme)))
                                      "KEYWORD"]
                                     [(and (string=? category "NUMBER_INT")
                                           (regexp-match? #rx"[jJ]$" lexeme))
                                      "NUMBER_COMPLEX"]
                                     [else category])]
                    [new-lines (count-char lexeme #\n)]
                    [new-line (if (> new-lines 0) (+ line new-lines) line)]
                    [new-col (if (> new-lines 0)
                                 (+ 1 (string-length (last (string-split lexeme "\n"))))
                                 (+ col lexeme-length))])
               (loop new-text 
                     (cons (list final-category lexeme line col) tokens)
                     new-line
                     new-col))
             (let ([unknown-char (substring remaining-text 0 1)])
               (loop (substring remaining-text 1)
                     (cons (list "UNKNOWN" unknown-char line col) tokens)
                     line
                     (+ col 1)))))])))

;; Función para escapar strings en CSV
(define (escape-csv-string str)
  (if (regexp-match? #rx"[\",\n]" str)
      (string-append "\"" (string-replace str "\"" "\"\"") "\"")
      str))

;; Función para escribir tokens a CSV - Formato simple para mejor compatibilidad
(define (write-tokens-to-csv tokens output-file)
  (with-output-to-file output-file
    #:exists 'replace
    (lambda ()
      ;; Usar un formato simple con solo tipo y lexema
      (displayln "tipo,lexema")
      (for-each
       (lambda (token)
         (let ([category (first token)]
               [lexeme (second token)])
           ;; Filtrar tokens problemáticos
           (unless (and (string=? category "UNKNOWN") 
                        (or (string=? lexeme "") (string=? lexeme "\n") (string=? lexeme "\r\n")))
             (printf "~a,~a\n" 
                     (escape-csv-string category)
                     (escape-csv-string lexeme)))))
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

;; Ejecutar el programa
(main)