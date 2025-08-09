# ¿Que es esto?
Una **pagina que muestra las mejores notebooks usadas de mercado libre ordenadas por precio / calidad**.\
En **mejores notebooks** se puede ver la lista filtrada para no mostrar las que tienen un puntaje menor a 40 o en su defecto que tengan un precio mas bajo que $150.000.\
En **lista completa** esta la lista sin ningun tipo de filtro, lo unico que saco son las publicaciones que venden repuestos.

# ¿Como funciona?
Funciona a traves de un script en python que, empezando por una busqueda inicial en la categoria notebooks, agarra todos los productos que se pueden ver en el listado de mercado libre, para cada uno saca titulo, precio, es promocionado o no y link al articulo, guarda el producto en un diccionario y lo mete en una lista.

Luego, iteramos por esa lista entrando a cada link agarrando descripcion y caracteristicas, usamos expresiones regulares para ordenar y sacar solo los datos que buscamos, le asignamos un puntaje en base y actualizamos el diccionario con toda la informacion.

El puntaje se consigue en base a las caracteristicas del producto, tiene en cuenta ram, cpu y generacion de cpu ya que estas son los datos que mas se encuentran en cada publicacion. Podria considerar tambien si es disco duro o ssd, espacio del disco, si es tactil, etc. pero todas estas caracteristicas no aparecen con tanta frecuencia.

Ahora que tenemos la lista con todos los productos y la informacion de cada uno, pasamos todo a json y lo guardamos en un archivo que despues vamos a usar para mostrar en la pagina.

# ¿Para que?
La idea inicial surge porque **necesitaba notebooks para ampliar mi cluster** y para eso sentia que comprar una notebook nueva era medio un desperdicio. Asi que empece a revisar mercado libre periodicamente en busca de buenas notebooks con buen precio y el proceso era **muy monotono y lento** ya que la ui estaba llena de cosas, **ademas de que para cada producto que me interesara tenia que**:

1. **entrar al articulo,** 
2. **buscar las caracteristicas que me importan,** 
3. **agregar el producto a favoritos asi lo puedo volver a encontrar rapidamente**
4. **volver para atras y seguir revisando el listado.**

El objetivo de esta pagina es:

- **Poder ver los productos mas interesantes primero,**
- **Tener todas las notebooks con su informacion mas importante en un mismo lugar,**
- **poder ver que productos ingresan, cuales estan hace mucho tiempo y cuales cambian de precio.**
# ¿Que falta?

- **Agregar la pagina que muestra productos que ingresan, que se venden, que cambiaron de precio HOY.**
- **Ampliar el programa para que funcione con mas marcas y modelos (Por ahora solo busca thinkpads y latitude)**
