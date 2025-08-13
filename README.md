
# ¿Qué es esto?
Una **página que muestra las mejores notebooks usadas de mercado libre ordenadas por precio / calidad**.\
En **mejores notebooks** se puede ver la lista filtrada para no mostrar las que tienen un puntaje menor a 40 o en su defecto que tengan un precio más bajo que $150.000.\
En **lista completa** esta la lista sin ningún tipo de filtro, lo unico que saco son las publicaciones que venden repuestos.

# ¿Cómo funciona?
Funciona a través de un script en python que, empezando por una búsqueda inicial en la categoría notebooks, agarra todos los productos que se pueden ver en el listado de mercado libre, para cada uno saca título, precio, es promocionado o no y link al artículo, guarda el producto en un diccionario y lo mete en una lista.

Luego, iteramos por esa lista entrando a cada link agarrando descripción y características, usamos expresiones regulares para ordenar y sacar solo los datos que buscamos, le asignamos un puntaje en base y actualizamos el diccionario con toda la información.

El puntaje se consigue en base a las características del producto, tiene en cuenta ram, cpu y generación de cpu ya que estos son los datos que más se encuentran en cada publicación. Podría considerar también si es disco duro o ssd, espacio del disco, si es táctil, etc. pero todas estas características no aparecen con tanta frecuencia.

Ahora que tenemos la lista con todos los productos y la información de cada uno, pasamos todo a json y lo guardamos en un archivo que después vamos a usar para mostrar en la página.

En este momento la pagina esta siendo hosteada en github pages, y es actualizada desde un container cada dos horas con un script corriendo en cron.

Todos los archivos que hacen funcionar a esta pagina se puede ver [aca](https://github.com/juan-martell/juan-martell.github.io)

# ¿Para qué?
La idea inicial surge porque **necesitaba notebooks para ampliar mi cluster** y para eso sentía que comprar una notebook nueva era medio desperdicio. Así que empecé a revisar mercadolibre periódicamente en busca de buenas notebooks con buen precio y el proceso era **muy monótono y lento** ya que la ui estaba llena de cosas, **además de que para cada producto que me interesara tenía que**:

1. **entrar al articulo,**
2. **buscar las características que me importan,**
3. **agregar el producto a favoritos asi lo puedo volver a encontrar rápidamente**
4. **volver para atrás y seguir revisando el listado.**

El objetivo de esta pagina es:

- **Poder ver los productos mas interesantes primero,**
- **Tener todas las notebooks con su información más importante en un mismo lugar,**
- **poder ver que productos ingresan, cuales están hace mucho tiempo y cuales cambian de precio.**
# ¿Qué falta?

- **Agregar la página que muestra productos que ingresan, que se venden, que cambiaron de precio HOY.**
- **Ampliar el programa para que funcione con mas marcas y modelos (Por ahora solo dell y lenovo)**
- **Mejorar el sistema que uso para determinar caracteristicas, haciendo que funcione por contexto (ej. si la linea es thinkbook entonces el modelo solo puede ser 13/14s)**
