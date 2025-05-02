### Ejercicios Python

import math

### Ejercicio 1

num1 = int(input("Ingresa primer Numero:"))
num2 = int(input("Ingresa segundo numero: "))

def suma(a, b):
    return a + b
print("El valor de la suma es:", suma(num1, num2))

### Ejercicio 2

def km_a_millas(km):
    return km * 0.621371

kilometros = float(input("Ingresa distancia en Kilometros: "))
millas = km_a_millas(kilometros)

print(f'{kilometros} kilometros son {millas} millas.')

### Ejercicio 3

def area_circulo(radio):
    return  math.pi * radio ** 2

radio = float(input("Ingresa el radio del circulo: "))

area = area_circulo(radio)

print(f'El area del circulo con radio {radio} es: {area:.2f}')