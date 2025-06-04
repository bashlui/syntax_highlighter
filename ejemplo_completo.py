#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejemplo completo para probar el resaltador de sintaxis
Este archivo contiene ejemplos de todas las categorías léxicas de Python
"""

# Importaciones
import os
import sys
from typing import List, Dict, Tuple, Optional

# Constantes
PI = 3.14159265359
MAX_VALUE = 1000
MIN_VALUE = -1000
NOMBRE = "Resaltador de Sintaxis"
HABILITADO = True
DESHABILITADO = False
VALOR_NULO = None

# Números en diferentes formatos
entero = 42
flotante = 3.14159
cientifico = 1.23e-4
hexadecimal = 0xFF
binario = 0b1010
octal = 0o755

# Función simple
def suma(a: int, b: int) -> int:
    """Suma dos números enteros"""
    return a + b

# Función con parámetros por defecto
def saludar(nombre: str = "Mundo") -> str:
    """Retorna un saludo personalizado"""
    return f"¡Hola, {nombre}!"

# Clase simple
class Persona:
    """Clase que representa a una persona"""
    
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad
    
    def presentarse(self) -> str:
        """Método para presentar a la persona"""
        return f"Hola, me llamo {self.nombre} y tengo {self.edad} años."
    
    @property
    def es_mayor_edad(self) -> bool:
        """Propiedad que indica si la persona es mayor de edad"""
        return self.edad >= 18

# Clase con herencia
class Estudiante(Persona):
    """Clase que representa a un estudiante"""
    
    def __init__(self, nombre: str, edad: int, carrera: str):
        super().__init__(nombre, edad)
        self.carrera = carrera
    
    def presentarse(self) -> str:
        """Método para presentar al estudiante"""
        return f"{super().presentarse()} Estudio {self.carrera}."

# Función lambda
cuadrado = lambda x: x ** 2

# Comprensión de listas
numeros = [1, 2, 3, 4, 5]
cuadrados = [x ** 2 for x in numeros if x % 2 == 0]

# Diccionario
persona = {
    "nombre": "Juan",
    "edad": 30,
    "profesion": "Ingeniero"
}

# Manejo de excepciones
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Operación finalizada")

# Condicionales
edad = 18
if edad >= 18:
    print("Es mayor de edad")
elif edad >= 13:
    print("Es adolescente")
else:
    print("Es niño")

# Bucles
for i in range(5):
    print(i)

contador = 0
while contador < 5:
    print(contador)
    contador += 1

# Operadores
a = 10
b = 20
suma = a + b
resta = a - b
multiplicacion = a * b
division = a / b
division_entera = a // b
modulo = a % b
potencia = a ** 2
negacion = -a

# Operadores de comparación
igual = a == b
diferente = a != b
mayor = a > b
menor = a < b
mayor_igual = a >= b
menor_igual = a <= b

# Operadores lógicos
and_op = True and False
or_op = True or False
not_op = not True

# Operadores de asignación
x = 10
x += 5
x -= 3
x *= 2
x /= 4

# Decorador personalizado
def mi_decorador(func):
    """Decorador de ejemplo"""
    def wrapper(*args, **kwargs):
        print("Antes de llamar a la función")
        resultado = func(*args, **kwargs)
        print("Después de llamar a la función")
        return resultado
    return wrapper

@mi_decorador
def funcion_decorada():
    """Función con decorador"""
    print("Función decorada")

# Llamada a la función decorada
funcion_decorada()

# Fin del archivo 