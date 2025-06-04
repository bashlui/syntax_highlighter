# Diseño de Autómatas Finitos para el Analizador Léxico de Python

Este documento describe los autómatas finitos no deterministas (NFAs) y deterministas (DFAs) que se utilizan para reconocer las diferentes categorías léxicas del lenguaje Python.

## 1. Modelo General

El analizador léxico implementa un modelo de autómatas finitos que reconoce cada categoría léxica de Python. Cada expresión regular definida en el programa se puede representar como un autómata finito.

## 2. Autómatas por Categoría Léxica

### 2.1 Palabras Reservadas (KEYWORD)

El autómata para palabras reservadas reconoce tokens como `if`, `else`, `for`, `while`, etc.

```
Estado inicial: q0
Estados finales: q1
Transiciones:
  - q0 --[a-zA-Z_]--> q1 (para cada palabra reservada)
  - q1 debe estar delimitado por espacios, operadores o delimitadores
```

### 2.2 Identificadores (IDENTIFIER)

El autómata para identificadores reconoce nombres de variables, funciones, etc.

```
Estado inicial: q0
Estados finales: q2
Transiciones:
  - q0 --[a-zA-Z_]--> q1
  - q1 --[a-zA-Z0-9_]--> q1
  - q1 --> q2 (cuando termina el identificador)
```

### 2.3 Números (NUMBER)

El autómata para números reconoce enteros, flotantes, y números en diferentes bases.

```
Estado inicial: q0
Estados finales: q3, q5, q8
Transiciones para enteros:
  - q0 --[0-9]--> q1
  - q1 --[0-9]--> q1
  - q1 --> q3 (entero)

Transiciones para flotantes:
  - q1 --["."]--> q4
  - q4 --[0-9]--> q5
  - q5 --[0-9]--> q5
  
Transiciones para notación científica:
  - q3/q5 --["e","E"]--> q6
  - q6 --["+"," -"]--> q7 (opcional)
  - q6/q7 --[0-9]--> q8
  - q8 --[0-9]--> q8

Transiciones para hexadecimales:
  - q0 --["0"]--> q9
  - q9 --["x","X"]--> q10
  - q10 --[0-9a-fA-F]--> q11
  - q11 --[0-9a-fA-F]--> q11
  
Transiciones para binarios:
  - q9 --["b","B"]--> q12
  - q12 --[0-1]--> q13
  - q13 --[0-1]--> q13
  
Transiciones para octales:
  - q9 --["o","O"]--> q14
  - q14 --[0-7]--> q15
  - q15 --[0-7]--> q15
```

### 2.4 Cadenas (STRING)

El autómata para cadenas reconoce diferentes tipos de cadenas en Python.

```
Estado inicial: q0
Estados finales: q2, q4
Transiciones para cadenas simples:
  - q0 --["'"]--> q1
  - q1 --[^'\n]--> q1
  - q1 --["'"]--> q2
  
Transiciones para cadenas dobles:
  - q0 --["\""]--> q3
  - q3 --[^"\n]--> q3
  - q3 --["\""]--> q4
  
Transiciones para cadenas triples (simples):
  - q0 --["'''"]--> q5
  - q5 --[cualquier caracter, incluidos saltos de línea]--> q5
  - q5 --["'''"]--> q6
  
Transiciones para cadenas triples (dobles):
  - q0 --["\"\"\""]--> q7
  - q7 --[cualquier caracter, incluidos saltos de línea]--> q7
  - q7 --["\"\"\""]--> q8
```

### 2.5 Comentarios (COMMENT)

El autómata para comentarios reconoce líneas que comienzan con #.

```
Estado inicial: q0
Estados finales: q2
Transiciones:
  - q0 --["#"]--> q1
  - q1 --[cualquier caracter excepto nueva línea]--> q1
  - q1 --[fin de línea]--> q2
```

### 2.6 Operadores (OPERATOR)

El autómata para operadores reconoce todos los operadores de Python.

```
Estado inicial: q0
Estados finales: q1, q2, q3
Transiciones para operadores simples:
  - q0 --[+,-,*,/,%,^,&,|,~,<,>,=]--> q1
  
Transiciones para operadores compuestos:
  - q0 --[*]--> q1
  - q1 --[*]--> q2 (para **)
  - q0 --[/]--> q1
  - q1 --[/]--> q2 (para //)
  - q0 --[=,!,<,>]--> q1
  - q1 --[=]--> q2 (para ==, !=, <=, >=)
  - q0 --[+,-,*,/,%,&,|,^,<,>]--> q1
  - q1 --[=]--> q2 (para +=, -=, etc.)
  - q0 --[*]--> q1
  - q1 --[*]--> q2
  - q2 --[=]--> q3 (para **=)
```

### 2.7 Delimitadores (DELIMITER)

El autómata para delimitadores reconoce caracteres especiales que delimitan estructuras.

```
Estado inicial: q0
Estados finales: q1
Transiciones:
  - q0 --[(,),{,},[,],,,.,;,:,@]--> q1
```

### 2.8 Decoradores (DECORATOR)

El autómata para decoradores reconoce anotaciones de función.

```
Estado inicial: q0
Estados finales: q2
Transiciones:
  - q0 --[@]--> q1
  - q1 --[a-zA-Z_]--> q2
  - q2 --[a-zA-Z0-9_]--> q2
```

## 3. Integración de Autómatas

El analizador léxico utiliza un enfoque de "competencia" entre los diferentes autómatas:

1. En cada posición del código fuente, se intenta aplicar cada autómata.
2. El autómata que consuma la secuencia más larga de caracteres "gana".
3. Si ningún autómata puede consumir caracteres, se trata como un carácter desconocido.

Este enfoque garantiza que los tokens se reconozcan correctamente incluso cuando hay ambigüedades (por ejemplo, entre palabras reservadas e identificadores).

## 4. Implementación en Racket

En la implementación en Racket, cada expresión regular representa implícitamente un autómata finito. El proceso de matching de estas expresiones regulares contra el texto de entrada simula la ejecución de estos autómatas.

La función `match-token` implementa la competencia entre autómatas al probar cada expresión regular en un orden específico y devolver el primer match exitoso. 