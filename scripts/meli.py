import requests, os, json, random
from bs4 import BeautifulSoup
from config import *
from filtrado import *

# FUNCIONES DE WEB SCRAPPING PARA LISTADOS DE ARTICULOS
def get_items_in_page(items) -> list[dict]: 
    '''
    items: es el objeto con todos los productos de la pagina 
    Agarra todos los productos de items y extrae 
    precio, link, titulo, si esta en descuento o no, si es publicidad, etc
    luego agrega todo eso como entry en un diccionario, tambien usa una funcion
    auxiliar para extraer informacion del titulo.
    '''
    res = []
    for i in range(len(items)):
        titulo: str = items[i].find('a', class_="poly-component__title").text.strip()
        res.append(pasar_de_item_a_diccionario(titulo, items[i]))
    return res

def pasar_de_item_a_diccionario(titulo: str, component) -> dict:
    res: dict = {}
    link: str = component.find('a', class_="poly-component__title")['href']
    precio_mas_descuento = component.find('div', class_="poly-price__current")
    precio: str = precio_mas_descuento.find('span', class_="andes-money-amount andes-money-amount--cents-superscript").text.strip()
    descuento = precio_mas_descuento.find('span', class_="andes-money-amount__discount")
    if descuento:
        descuento = descuento.text.strip()
    else:
        descuento = "0% OFF"
    promocionado: bool = bool(component.find('a', class_="poly-component__ads-promotions"))
    res: dict = {
        'titulo': titulo,
        'precio': int(precio.replace(".", "").replace("$", "")),
        'descuento': descuento,
        'link': link,
        'es_promocionado': promocionado,
        'disponible': True,
        'precios_anteriores': [],
        'fecha_agregado': fecha,
        'ultimo_cambio': '',
    }
    print("-> " + titulo)
    return res

def get_all_resultados(url, headers) -> list[dict]:
    '''
        arma las url de las paginas con todos los productos y va agregando
        cada producto que encuentra en una lista. Tengo que ir contando
        el index de 50 en 50 porque esa es la cantidad de items que muestra
        por pagina mp.
    '''
    res: list[dict] = []
    index: int = 1
    count: int = 1
    while True:
        url_real: str = url + "_Desde_" + str(index) + "_NoIndex_True?sb=all_mercadolibre"
        try:
            response = requests.get(url_real, headers=headers) # Hacemos la request y nos devuelve el html
        except requests.exceptions.RequestException as e:
            print(f"Error en la request a {url_real}: {e}")
            return res
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('li', class_='ui-search-layout__item')
        if not items:
            break
        else:
            pagina: list[dict] = get_items_in_page(items)
            for item in pagina:
                res.append(item)
            print(f"-> pagina {count} terminada...")
        count += 1
        index += 50
    return res

# FUNCIONES PARA GUARDAR, CARGAR Y ACTUALIZAR JSON 
def guardar_json(l:list[dict], nombre_archivo: str) -> None:
    '''Guarda una lista de json en un archivo'''
    with open(nombre_archivo, "w") as f:
        for prod in l:
            f.write(json.dumps(prod, ensure_ascii=True) + "\n")

def abrir_json(nombre_archivo: str) -> list[dict]:
    '''Lee el archivo que le pasas como lista de jsons y lo devuelve como lista de diccionarios'''
    res: list[dict] = []
    with open(nombre_archivo, "r") as f:
        for linea in f:
            if linea.strip():
                res.append(json.loads(linea))
    return res

def actualizar_diccionario(actual: list[dict], viejo: list[dict]) -> list[dict]:
    ''' 
        Si el producto cambia su precio, agrega el precio anterior a una lista
        Si el producto se vende, disponible == False
        si el producto cambia precio o se vende, ultimo_cambio == fecha actual 
        se asegura de que los productos que se vendieron queden en el diccionario
        por si vuelven a ser publicados y para tener mas info de que se vendio y
        que se modifico.
    '''
    res: list[dict] = []
    for descripcion in viejo:
        titulo: str = descripcion["titulo"]
        encontrado: bool = False
        for j in actual:
            if j["titulo"] == titulo and not filtrar_por(res, "titulo", lambda x: x == titulo):
                encontrado = True
                precio_viejo: int = descripcion["precio"]
                precio_actual: int = j["precio"]
                j["fecha_agregado"] = descripcion["fecha_agregado"]
                if precio_actual != precio_viejo:
                    j["precios_anteriores"].append(precio_viejo)
                    j["ultimo_cambio"] = fecha
                res.append(j)
        if not encontrado:
            descripcion["disponible"] = False
            descripcion["ultimo_cambio"] = fecha 
            res.append(descripcion)    
    for descripcion in actual:
        titulo: str = descripcion["titulo"]
        en_res: bool = bool(filtrar_por(res, "titulo", lambda x: x == titulo))
        if not en_res:
            res.append(descripcion)
    return res
                
def sacar_duplicados(nombre_archivo:str) -> list[dict]:
    '''abre el archivo, saca elementos duplicados, y devuelve la lista, si no existe devuelve lista vacia'''
    res: list[dict] = []
    if os.path.exists(nombre_archivo):
        aux = abrir_json(nombre_archivo)
        sin_duplicar = []
        for i in aux:
            titulo = i["titulo"]
            if not filtrar_por(sin_duplicar, "titulo", lambda x: x == titulo):
                sin_duplicar.append(i)
        res = sin_duplicar
    return res

def main(l: list[str]) -> list[dict]:
    '''
    l: listado de nombres de productos
    agarra todos los items publicados en mercado libre con el nombre de producto
    que le pasaste, le arma un json a cada uno y lo guarda en un archivo     
    '''
    res: list[dict] = []
    # pagina a scrapear, en este caso meli
    base = 'https://listado.mercadolibre.com.ar'
    categoria = '/computacion/laptops-accesorios/notebooks/' 
    for i in l:
        url = base + categoria + i 
        lista_resultados = get_all_resultados(url, headers)
        for item in lista_resultados:
            res.append(item)
    if os.path.exists(nombre_archivo):
        res_viejo: list[dict] = sacar_duplicados(nombre_archivo)
        res = actualizar_diccionario(res, res_viejo)
    guardar_json(res, nombre_archivo)
    return res

# FUNCIONES DE WEB SCRAPPING PARA CADA PRODUCTO
def get_article(d: dict, headers=lista_headers[0]) -> dict[str, str|int]:
    ''' 
        Hace una request a la url que le das (un articulo de meli) y busca dentro de las tag script
        la que es solamente json, ya que aca estan las caracteristicas del producto, y se la pasa
        a una funcion auxiliar que procesa la info y devuelve eso
        Es medio un quilombo esta funcion. 
    '''
    res: dict = {
    }
    url: str = d["link"]
    try:
        response = requests.get(url, headers=headers, timeout=10) # Hacemos la request y nos devuelve el html
    except requests.exceptions.RequestException as e:
        print(f"Error en la request a {url}: {e}")
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find_all('script')
    for script in script_tag:
        if "pageState" in script.text.strip():
            try:  
                data = json.loads(script.text.strip())
                for key, value in d.items():
                    if key not in ["promocionado", "descuento"]:
                        res[key] = value
                res.update(get_caracteristicas_in_article(data))
                res["modelo"] = regex_caracteristicas(d["titulo"], "modelo")
                res["ram"] = agregar_ram(res)
                res["cpu"] = agregar_procesador(res)
                res["cpu_gen"] = agregar_generacion(res)
                res["score"] = agregar_puntaje(res)
            except json.JSONDecodeError:
                continue
    return res

def get_caracteristicas_in_article(data: dict) -> dict[str, str]:
    res: dict[str, str] = {}
    nombre_caracteristicas_en_articulo: dict = {
        'marca': 'Marca',
        'linea': 'Línea',
        'modelo': ['Modelo', 'Modelo alfanumérico'],
        'marca_procesador': 'Marca del procesador',
        'linea_procesador': 'Línea del procesador',
        'modelo_procesador': 'Modelo del procesador',
        'nucleos': 'Cantidad de núcleos',
        'marca_tarjeta_grafica': 'Marca de la tarjeta gráfica integrada',
        'linea_tarjeta_grafica': 'Linea de la tarjeta gráfica integrada',
        'bateria': 'Duración máxima de la batería',
        'ram': 'Capacidad total del módulo de memoria RAM',
        'tipo_de_ram': 'Tipo de memoria RAM',
        'disco': ['Capacidad del disco rígido', 'Capacidad de disco SSD']
    }
    if 'description' in data['pageState']['initialState']['components'].keys() and 'content' in data['pageState']['initialState']['components']['description'].keys():
        descripcion: str = data['pageState']['initialState']['components']['description']['content']
        res["descripcion"] = descripcion.replace("\n", " ").strip()
    if 'components' in data['pageState']['initialState']['components']['highlighted_specs_attrs'].keys():
        highlights: list[dict] = data['pageState']['initialState']['components']['highlighted_specs_attrs']['components']
    else:
        return res
    for i in highlights:
        if 'specs' in i.keys():
            specs = i['specs']
            break
    for i in specs:
        attr: list[dict[str, str]] = i['attributes']
        for j in attr:
            attr_nombre = j["id"]
            attr_text = j["text"]
            for key, value in nombre_caracteristicas_en_articulo.items():
                if (type(value) == str and attr_nombre == value) or (key == 'modelo' and attr_nombre in value) :
                    res[key] = attr_text
                elif key == 'disco' and attr_nombre in value:
                    res[key] = attr_text
    return res

def agregar_generacion(d: dict) -> int:
    gen: int = 0
    tries = 0
    while tries < 3 and gen == 0:
        if "modelo_procesador" in d.keys() and tries == 0:
            gen = regex_generacion(d["modelo_procesador"])
        elif "linea_procesador" in d.keys() and tries == 1:
            gen = regex_generacion(d["linea_procesador"])
        else:
            gen = int(regex_caracteristicas(d["titulo"], "gen"))
        tries += 1
    return gen

def agregar_procesador(d: dict) -> str:
    tries = 0
    proc = ""
    while tries < 3 and proc == "":
        if "linea_procesador" in d.keys() and tries == 0:
            proc = regex_procesador(d["linea_procesador"])
        elif "modelo_procesador" in d.keys() and tries == 1:
            proc = regex_procesador(d["modelo_procesador"])
        else:
            proc = regex_procesador(d["titulo"])
        tries += 1
    return proc

def agregar_ram(d: dict) -> int:
    tries = 0
    ram: int = 0
    while tries < 3 and ram == 0:
        if "ram" in d.keys() and tries == 0:
            ram = int(regex_caracteristicas(d["ram"], "RAM"))
        else:
            ram = int(regex_caracteristicas(d["titulo"], "ram"))
        tries +=1
    return ram
 
def agregar_puntaje(descripcion: dict) -> int:
    '''
        Asigna un puntaje en base a cant. de ram, procesador y generacion de procesador 
        Devuelve ese numero y cambia el valor en el diccionario q le pasas
    '''
    cpu: str = descripcion["cpu"]
    gen: int = descripcion["cpu_gen"]
    ram: int = descripcion["ram"]
    puntaje: int = 0 
    cpu_base_score = {
        'I7': 30,
        'I5': 20,
        'I3': 10,
        'CELERON': 5,
        'CORE 2 DUO': 5,
        'CENTRINO': 5,
        'RYZEN 7 PRO': 35,
        'RYZEN 7': 30,
        'RYZEN 5 PRO': 25,
        'RYZEN 5': 20,
        'RYZEN 3': 10,
        'R5': 20,
        'R7': 30,
        'R4': 15,
        'XEON': 7,
    }
    puntaje = cpu_base_score.get(cpu, 5)
    if descripcion.get("marca_procesador", "").upper() == "AMD":
        gen += 6
    if gen >= 10:
        puntaje += round(gen*2)
    elif gen >= 8:
        puntaje += round(gen*1.5)
    else:
        puntaje += 1
    if ram >= 8:
        puntaje += round(ram*0.5)
    else:
        puntaje += 1
    descripcion["score"] = puntaje
    return puntaje

def guardar_todas_las_paginas(d: list[dict]) -> list[dict]:
    '''
        guarda todos los articulos una lista de diccionarios
        si el articulo esta en d pero no en el nombre_articulo lo agrega a archivo
        si el articulo esta en nombre_articulo lo actualiza con la nueva info en d
        si get_article devuelve dict vacio o se agregaron 20 articulos cambia la vpn
    '''
    agregados: int = 0 
    articulos: list[dict] = sacar_duplicados(nombre_articulo)
    faltan_agregar: list[dict] = articulos_que_faltan(d, articulos)
    if faltan_agregar: 
        print(f"> Agregando {len(faltan_agregar)} articulos")
    for i in range(len(faltan_agregar)):
        h = random.choice(lista_headers)
        articulo = get_article(faltan_agregar[i], h)
        titulo = articulo["titulo"]
        articulos.append(articulo)
        print(f"> Articulo agregado {titulo}")
        agregados += 1
        guardar_json(articulos, nombre_articulo)
    guardar_json(articulos, nombre_articulo)
    print("> Todos los articulos agregados!")
    return articulos


def articulos_que_faltan(d: list[dict], articulos: list[dict]) -> list[dict]:
    '''devuelve una lista con los articulos que falta agregar y actualiza los que ya existen'''
    res: list[dict] = []
    for descripcion in d:
        titulo = descripcion["titulo"]
        existe: list[dict] = filtrar_por(articulos, "titulo", lambda x: x == titulo)
        if not existe: # Si el diccionario no esta en articulos lo metemos en la lista 
            res.append(descripcion)
        else: # si esta lo actualizamos
            articulo = existe[0]
            articulo["fecha_agregado"] = descripcion["fecha_agregado"]
            articulo["disponible"] = descripcion["disponible"]
            articulo["link"] = descripcion["link"]
            articulo["precios_anteriores"] = descripcion["precios_anteriores"]
            articulo["ultimo_cambio"] = descripcion["ultimo_cambio"] 
    return res

def lista_caracteristicas(d: list[dict], car: str) -> tuple[list[str|int],int]:
    ''' devuelve una tupla con la lista de todos los posibles valores de la key car y el numero de productos que no decian nada'''
    res = []
    no_dice = 0
    for value in d:
        if car not in value.keys() or value[car] == 0 or value[car] == "":
            no_dice += 1
        elif type(value[car]) == str and value[car].upper() not in res:
            res.append(value[car].upper())
        elif type(value[car]) == int and value[car] not in res:
            res.append(value[car])
    return (res, no_dice)

def imperdible(d:list[dict]) -> list[dict]:
    ''' 
        Asigna un puntaje a cada producto.
        Luego en base a el puntaje y su precio devuelve una lista con los mejores productos
        mejores productos: con puntaje mayor a 40 o con precio menor a 150mil
    '''
    aux = filtrar_de_reparacion(filtrar_por(d, "disponible", lambda x: x == True))
    for i in aux:
        if i.get("disponible", True):    
            i.pop("descripcion", "")
            i.pop("marca_tarjeta_grafica", "")
            i.pop("tipo_de_ram", "")
            i.pop("linea_procesador", "")
            i.pop("modelo_procesador", "")
            i.pop("marca_procesador", "")
            i.pop("es_promocionado", "")
            i.pop("precios_anteriores", "")
            i.pop("ultimo_cambio", "")
    top = sorted(aux,key=lambda x: x["precio"]/x["score"], reverse=False)
    res = []
    for i in top:
        if i["score"] >= 40 or i["precio"] < 150000:
            res.append(i)
    return res
            
def cambiar_formato_fecha(fecha: str) -> int:
    aux = fecha.split('/')
    dia = aux[0]
    mes = aux[1]
    anio = aux[2]
    numero = int(anio+mes+dia)
    return numero

# notebooks = main(paginas_articulos)
# articulos = guardar_todas_las_paginas(notebooks)
# top = imperdible(articulos)
# guardar_json(top, archivo_top)
articulos = abrir_json(nombre_articulo)
nuevas = sorted(articulos, key=lambda x: cambiar_formato_fecha(x['fecha_agregado']), reverse=True)
vendidas = sorted(filtrar_por(articulos, "disponible", lambda x: x == False), key=lambda x: cambiar_formato_fecha(x['ultimo_cambio']), reverse=True)
guardar_json(nuevas[:20], 'nuevos_ingresos.json')
guardar_json(vendidas[:20], 'ultimas_ventas.json')

    



