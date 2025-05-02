### Ejercicio 5

segundos = int(input('Ingresa el numero de segundos: '))

horas = segundos // 3600
minutos = (segundos % 3600) // 60
segundos_restantes = segundos % 60

print(f"{segundos} segundos son {horas} horas, {minutos} minutos y {segundos_restantes} segundos.")

### Ejercicio

numero =  float(input('Ingresa un numero: '))

if numero > 0:
    print('El numero es positivo')
elif numero< 0:
    print('El numero es negativo')
else:
    print('El numero es cero')
    
