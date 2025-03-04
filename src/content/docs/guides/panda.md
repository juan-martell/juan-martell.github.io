---
title: Panda
description: 22/10/2024
---
Panda es una libreria de python que se usa para armar bases de datos. es facil y rapida.

> import pandas as pd 

# DataFrames
Es la estructura de datos que se usa en panda. matrices bidimensionales con filas y
columnas. Muchas funciones para filtrar y seleccionar datos.
Para armar un Dataframe necesitamos 2 [diccionarios](/diccionarios.md):
    * Uno con las filas y las columnas que queremos mostrar.
    * Otra con los indices que pensamos utilizar.
```python
 data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat',
'dog', 'dog'],
'age': [2.5, 3, 0.5, None, 5, 2, 4.5, None, 7, 3],
'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no',
'no']}
 labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
```
Ahora creamos el diccionario y lo mostramos en pantalla:
```python
df = pd.DataFrame(data, index=labels)             # type: ignore
print(df)
```
## Metadata
Si queremos mostrar informacion sobre el dataframe en si, usamos 2 funciones:}

    1. df.info() = Muestra info sobre indices, columnas, valores no nulos
    y uso de memoria

> print(df.info())

    2. df.describe() = Muestra numero de datos, la suma, minimo, maximo, media,
    cuartile y desviacíon tipica.

> print(df.describe())

# Display dentro de la Base de Datos
## Tail & Head
Concepto que ya conocemos de bash, **tail** se usa para mostrar los ultimos valores en el
documento, **head** se usa para mostrar los **primeros**   

> df.tail(3)

> df.head(6)

## Busquedas dentro del Dataframe
Panda nos permite mostrar y buscar valores con niveles de complejidad tremendos, por ende 
pienso separar esto en 2 niveles para tenerlo un poco mas ordenado.

### Busqueda simple
Cuando nosotros ya conocemos el index y lo queremos mostrar
podemos usar 2 funciones que son claves y super flexibles en panda:

> df.iloc[:]
> df.loc[:]

En este estado, las funciones funcionan como un slice [n:m] en la que n es el primer indexque se muestra y m es hasta q index mostrar sin incluirlo. En el codigo q mostramos le 
estamos diciendo a la funcion que muestre **TODO** el dataframe. Tambien lo podemos usar
exactamente igual que head haciendo [:3] (mostrar los primeros 3 valores) o que tail [2:]
(mostrar todos los valores menos los primeros 2).
Si ahora, nosotros queremos mostrar **solamente** n cantidad de columnas podemos usar las 
mismas funciones de antes, pero aca se empiezan a notar sus diferencias. 
Si queremos usar el numero de index podemos hacer:

> df.iloc[:, [0,1]]    #    mostrar todas las filas pero solo las columnas 0 y 1 

Si queremos usar el nombre de las columnas hacemos:

> df.loc[:, ["animal", "age"]]  #  mostrar todas las filas pero solo las columnas 0 y 1

> [!Observacion]
> si queremos mostrar la lista completa tmb podemos hacer iloc o loc con un empty array como en el ejemplo anterior.

## Busqueda compleja 
Tan compleja no es, pero es confusa por el doble nesting y todas esas cosas, ya te vas a 
dar cuenta.
Si queremos mostrar un index en especifico podemos usar otra funcion, **df.index[]**. 
Por si sola esta funcion solo nos devuelve el valor del index del numero que le pasemos,
pero si la usamos en combinacion con las cosas que ya conocemos podemos cosas mas utiles:

> df.loc[df.index[1]]   # muestra el animal en el index 1 con las columnas como filas

> df.loc[df.index[[3, 4, 8]], "animal"] #Muestra nombre de los animales indicados x index

## Operadores
Si queremos mostrar solo los animales que tengan una cierta edad podemos usar operadores
como **== , >, <** dentro de df.

> df[df["visits"] > 3]      # Mostrar los animales con un numero de visitas mayor a 3

> [!Observacion]
> df["visits"] solo nos devuelve el nombre de la columna y su tipo

> df[df["animal"] == "cat"] # Mostrar solo los gatos

Otras funciones que no son operadores pero que simplifican busquedas que podriamos hacer
solo usando operadores son .isnull() y .between:

> df["age"].isnull()]   # Todos los animales que tienen none en la columna edad

> df["visits".between(1, 3)] # todos los animales que tengan 1 y 3 en columna visitas

## Combinar mas de un operador 
Si necesitamos hacer mas complicada nuestra busqueda de lo que ya es, panda nos da esa 
posibilidad con el operador **&** que se utiliza para unir 2 querys y podemos usar mas 
de una vez.

> df[(df['animal'] == 'cat') & (df['age'] < 3)]) # muestra gatos con edad menor a 3

# Agregar y sacar valores en nuestro DataFrame
Super simple, hay varias formas. 
Si se quiere cambiar un valor que ya existe hacemos:

> df.loc['f', 'age'] = 1.5

Si lo que buscamos es agregar un valor nuevo:

> df.loc['k'] = ['dog', 5.5, 2, 'no']

Para eliminar una fila: 

> df.drop("k") 

Cambiar todas las apariciones de un valor por otro, aca tenemos 2 opciones, si solo es 
uno el valor que queremos cambiar usamos:

> df['animal'] = df['animal'].replace('snake', 'python')

Si tenemos que cambiar mas de una palabra a la vez usamos:

> df['priority'] = df['priority'].map({'yes': True, 'no': False}) # cambia todas las instancias de yes y de no por true y false en la columna priority

## Mas funciones random que se usan bastante
Suma de todos los valores dentro de una columna:

> df["age"].sum()

Hacer la media de valores dentro de una columna:

> df["visits"].mean()

Media de visitas pero se muestra por animal:

> df.groupby('animal')["visits"].mean()









