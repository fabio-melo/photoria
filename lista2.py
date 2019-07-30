#lista2.py

# PS: PRINTS NO ESTILO PYTHON 3.6+

# questaõ 1
f = int(input("digite a temp em farenheit"))
c = 5 * (f - 32) / 9
print(f"Temperatura em Celsius {c}")

# questão 2

var1 = int(input()) 
var2 = int(input())

temp = var1
var1 = var2
var2 = var1
print(f"{var1} - {var2}")

# questão 3
num = int(input())
if (num % 2 == 0):
  print("é par")
else:
  print("é impar")

maior = num1 if ((num1 > num2) and (num1 > num3)) else num2 if ((num2 > num1) and (num2 > num3)) else num3 if ((num3 > num1) and (num3 > num2)) else num1;

#questao 4

n1,n2,n3 = input(), input(),input()

def comparar(n1,n2,n3):
  if n1 == n2 == n3: print("tudo igual")
  elif n1 > n2: # essa linha precisa identar
    if n1 > n3: print("o maior é o n1") # já essa não 
    else: print("o maior é o n3")
  else:
    if n2 > n3: print("o maior é o n2")
    else: print("o maior é n3")

# questão 5

valor_salario = int(input())

if valor_salario < 420:
  inss = valor_salario * 0.08
elif (valor_salario > 420) and (valor_salario < 1350):
  inss = valor_salario * 0.09
else:
  inss = valor_salario * 0.1

valor_liquido = valor_salario - inss
print(f"INSS: {inss}, Valor Liquido: {valor_liquido}")

# QUestão 6

#%%
n = 10
a,b = 1,1
for x in range(n):
  c = a + b
  a = b
  b = c
    

