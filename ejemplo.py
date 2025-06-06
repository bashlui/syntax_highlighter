
"""
Este es un ejemplo que muestra todos los tipos de tokens en Python
para probar el analizador léxico.
"""

def ejemplo_keywords():
    if True:
        pass
    elif False:
        pass
    else:
        pass
    
    for i in range(10):
        continue
    
    while False:
        break
    
    try:
        raise Exception()
    except Exception as e:
        pass
    finally:
        pass
    
    class MiClase:
        def __init__(self):
            self.valor = None
    
    return lambda x: x + 1

variable_normal = 10
_variable_con_guion_bajo = 20
CamelCase = 30
snake_case_variable = 40

entero = 42
entero_negativo = -42
entero_grande = 1000000

flotante = 3.14
flotante_notacion = 1.5e10
flotante_negativo = -0.5

hexadecimal = 0xFF
binario = 0b1010
octal = 0o755
complejo = 3+4j

cadena_simple = 'Esto es una cadena con comillas simples'
cadena_doble = "Esto es una cadena con comillas dobles"
cadena_triple = """Esta es una cadena
con múltiples líneas
usando comillas triples dobles"""
cadena_triple_simple = '''Otra cadena
con múltiples líneas
usando comillas triples simples'''
cadena_f = f"El valor es {variable_normal}"

suma = 5 + 3
resta = 5 - 3
multiplicacion = 5 * 3
division = 5 / 3
division_entera = 5 // 3
modulo = 5 % 3
potencia = 5 ** 3

igual = 5 == 3
diferente = 5 != 3
mayor = 5 > 3
menor = 5 < 3
mayor_igual = 5 >= 3
menor_igual = 5 <= 3

and_logico = True and False
or_logico = True or False
not_logico = not True

x = 10
x += 5
x -= 2
x *= 3
x /= 2
x //= 2
x %= 3
x **= 2

bit_and = 5 & 3
bit_or = 5 | 3
bit_xor = 5 ^ 3
bit_not = ~5
bit_shift_left = 5 << 1
bit_shift_right = 5 >> 1

lista = [1, 2, 3]
tupla = (1, 2, 3)
diccionario = {"clave": "valor"}
conjunto = {1, 2, 3}
llamada_funcion = print("Hola")
indice = lista[0]
atributo = objeto.atributo
punto_y_coma = 1; 2
dos_puntos = {"a": 1}
    
@property
def mi_propiedad(self):
    return 42

resultado = len([1, 2, 3])
print(f"La longitud es: {resultado}")
valores = list(range(10))
maximo = max(valores)
minimo = min(valores)

