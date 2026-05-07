'''
    Seja d(n) definida como a soma dos divisores próprios de n (números menores que n que dividem n exatamente).
    Se d(a) = b e d(b) = a, onde a e b, então a e b são um par amigável e cada um de a e b é chamado de número amigável.
    Por exemplo, os divisores próprios de 220 são 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 e 110; 
    portanto, d(220) = 284. Os divisores próprios de 284 são 1, 2, 4, 71 e 142; então d(284) = 220.
    Avalie a soma de todos os números amigáveis ​​abaixo de 10000.
'''

cache = {}

def sum_div(n):
    if n in cache:
        return cache[n]
    
    if n == 1:
        return 0
    
    soma = 1
    
    for d in range(2, int(n**0.5)+ 1):
        if n % d == 0:
            soma += d
            if d != n //d:
                soma += n // d
                
    cache[n] = soma
    return soma

friendly = set()
LIMITE = 10000

for a in range(2,LIMITE):
    b = sum_div(a)
    
    if b != a and 1 < b < LIMITE and sum_div(b) == a:
        friendly.add(a)
        friendly.add(b)
        
print(sum(friendly))
        