# Ejemplo de código Python
def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@decorator
class MiClase:
    def __init__(self, valor=42):
        self.valor = valor * 3.14159
        
# Números en diferentes bases
hex_num = 0xFF
bin_num = 0b1010
oct_num = 0o755
sci_num = 1.23e-4