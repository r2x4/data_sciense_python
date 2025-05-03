### Ejercicio 5

segundos = int(input('Ingresa el numero de segundos: '))

horas = segundos // 3600
minutos = (segundos % 3600) // 60
segundos_restantes = segundos % 60

print(f"{segundos} segundos son {horas} horas, {minutos} minutos y {segundos_restantes} segundos.")

### Ejercicio

numero = float(input('Ingresa un numero: '))

if numero > 0:
    print('El numero es positivo')
elif numero < 0:
    print('El numero es negativo')
else:
    print('El numero es cero')

### Ejercicio 7

letra = input('Ingresa una letra: ').lower()

if len(letra) == 1 and letra.isalpha():
    if letra in 'aeiou':
        print('Es una Vocal')
    else:
        print("Es una consonante")
else:
    print("Entrada no valida. Debes  ingresar una  solo una letra")

### Ejercicio 6
## calculadora basica

num1 = float(input('Ingresa primer numero: '))
num2 = float(input('Ingresa Segundo numero: '))
operacion = input('Ingrese operacion en texto en minus.: ')
resultado = 0
if operacion == 'suma':
    resultado = num1 + num2
elif operacion == 'resta':
    resultado = num1 - num2
elif operacion == 'multiplicacion':
    resultado = num1 * num2
elif operacion == 'division':
    resultado = num1/num2
elif operacion == 'potencia':
    resultado = num1 ** num2
else:
    print('Ingrese una operacion valida')

print(f'el resultado de la {operacion} es: {resultado}')

