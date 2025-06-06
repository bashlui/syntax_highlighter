def fibonacci(n):
    """
    Genera los primeros n números de la serie de Fibonacci.
    
    Args:
        n: Cantidad de números de la serie a generar
        
    Returns:
        Una lista con los primeros n números de la serie
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib

if __name__ == "__main__":
    n = 10
    resultado = fibonacci(n)
    print(f"Los primeros {n} números de la serie de Fibonacci son:")
    print(resultado)
