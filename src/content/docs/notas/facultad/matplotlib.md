---
title: Matplotlib
description: 22/10/2024
---
Es la mas usada en el area probablemente, super simple, lo corres y te abre el grafico 
que le pediste. Pero para eso necesitamos una interfaz grafica.

# Pyplot
Pyplot es esa interfaz grafica que queriamos

> import matplotlib.pyplot as plt 

# Conceptos importantes

## Figure
Una figura es el marco que delimita la zona en la que trazamos el grafico, osea es la 
ventana que se crea cuando corremos el codigo. 

## Axes
Seria como los graficos, areas en la que los puntos se pueden mostrar en terminos de 
coordenadas. 
**Una figura puede tener muchos Axes pero un Axes solo puede tener una figura**

# Funciones principales
## plot y show
**Plot** es una funcion de pyplot que vamos a usar para unir puntos en el plano 
cartesiano
Para usarla necesitamos 2 vectores del mismo tamaño, cada uno representando un eje, con 
puntos que queremos mostrar. Luego la funcion agarra cada elemento de un eje y lo une con
el mismo elemento del siguiente eje y crea un punto que despues es conectado con el resto 
de puntos que crea.
**Show** muestra todos los elementos creados

> x = [0,2,10,11,18,25]                                                             
> y = [0,1,2,3,4,5]                                                                 
> fig = plt.figure()        # Creamos una ventana vacia                             
> plt.plot(x, y)            # Agregamos un grafico                                  
> plt.show()                # Lo mostramos en la ventana                            

## Otra forma de hacer lo mismo
El grafico que nos mostraba el codigo anterior tambien se puede mostrar de la siguiente
forma:

> x = [0,2,10,11,18,25]                                                             
> y = [0,1,2,3,4,5]                                                                 
> fig, ax = plt.subplots()  # Creamos una figura con solo 1 axes                    
> ax.plot(x, y)             # agregamos el grafico                                  
> plt.show()                # Lo mostramos en la ventana                            

Es lo mismo solo que esta forma es un poco mas flexible.

# Temas Aestethic
## linea
Para cambiar esas boludeces esteticas tenemos q cambiar parametros dentro de **ax.plot()**.
Parametros que acepta:
    * color = 'blue', 'green', 'red'
    * marker = '^', 'o', 'v' (como se marca un punto)
    * linestyle = '-', '--', ':'
    * marksize, linewidth = int (tamaño de la marca, ancho de la linea)
    * label = nombre de la linea, importantisimo si tenemos mas de una

> ax.plot(x, y, color='red', marker='o', linestyle=':', marksize=5)

## Cuadrilla
Podemos agregar una grilla para que se lea mejor el grafico con la funcion **ax.grid()**.
la grilla por default esta buena, pero tambien la podemos modificar:

> ax.grid(axis="both", color='gray')

## Titulos
Agregar titulos a los ejes y al grafico en general para que se entienda mejor q esta pasando.

> ax.set_title("grafico 1")
> ax.set_xlabel("eje x")
> ax.set_ylabel("eje y")

## legend
Agrega una referencia con el nombre de cada linea en pantalla y un simbolo
caracteristico.

> ax.legend()

# Otros tipos de grafico
Todo lo que vimos antes dependia de la funcion **Ax.plot()**, la utilidad de esta es crear
un solo tipo de grafico llamado "grafico de linea", pero tenemos mas opciones que se usan
en casos mas especificos y usan otras funciones:
    * grafico de Puntos = ax.scatter()
    * grafico de Barras vertical = ax.bar()
    * grafico de Barras horizontal = ax.hbar()
    * grafico de torta = ax.pie()

**Tener en cuenta que todas estas funciones pueden aceptar los parametros de ax.plot()**

## Varias curvas en un mismo grafico 
super simple, usas el mismo ax.plot() pero con diferentes valores:

> x = []
> y_linear = []
> y_cuadratica = []
> y_cubica = []
> fig, ax = plt.subplots(figsize=(5, 3))
> ax.plot(x, y_linear, label="lineal")
> ax.plot(x, y_cuadratica, label="cuadratica")
> ax.plot(x, y_cubica, label="cubica")
> ax.set_title("Grafico de multiples curvas")
> ax.set_xlabel("x")
> ax.set_ylabel("y")
> ax.legend()
> plt.show()

## varios graficos en una misma ventana
Tambien super simple, hay que entender los plots como matriz y los subplots como valores
dentro de esa matriz, por ende para hacer varios graficos solo tenemos q especificar el 
numero de filas y de columnas que queremos, esto se hace con:

> plt.subplots(nrows=n, ncols=n)

Y para agregar una curva en un espacio dentro de esa matriz hacemos:

> ax[n, n].plot(x, y)

Entonces si usamos los valores x e y del anterior ejemplo podemos hacer:

> fig, ax = plt.subplots(nrows=3, ncols=1)
> ax[0].plot(x, y_linear)
> ax[0].set_title("Lineal")
> ax[1].plot(x, y_cuadratica)
> ax[1].set_title("Cuadratica")
> ax[2].plot(x, y_cubica)
> ax[2].set_title("Cubica")
> plt.show()

# Graficos para un [Dataframe](/panda.md)
Si tenemos un dataframe, en la facu usamos [panda] para eso, podemos usar la informacion
que tenemos ahi para armar algun grafico interesante.

> import panda as pd 
> data = {'animal': ['cat','snake', 'dog'], 'age': [2.5, 3, 7]}
> df = pd.DataFrame(data)
> x = df['animal']
> y = df['age']
> fig, ax = plt.subplots()
> ax.bar(x, y)
> ax.set_xlabel('Animal')
> ax.set_ylabel('Age')
> ax.set_title('Mascotas')
> plt.show()

