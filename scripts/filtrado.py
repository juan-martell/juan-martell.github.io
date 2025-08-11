from typing import Callable
from config import fecha
import re
# funciones boludas

def filtrar_por(d: list[dict], llave: str, condicion: Callable[[int], bool]) -> list[dict]:
    '''
       Crea otro diccionario con los productos que cumplen la condicion (uso lo de Callable pq sino me tiraba un error).
       ejemplos de condicion: 
            - agarra todos los productos cuyo modelo sea T490 
            filtrar_por(productos, "modelo", lambda x: x == "T490")
            - agarra todos los productos cuyo precio sea menor a 200.000
            filtrar_por(productos, "precio", lambda x: x < 200000)
    '''
    res: list[dict] = []
    for i in d:
        if condicion(i[llave]):
            res.append(i)
    return res
 
def cuales_matchean(d: list[dict], llave: str, que_buscas) -> list[dict]:
    return filtrar_por(d, llave, lambda x: x == que_buscas)
 
def maxmin_precio(d: list[dict], maximo: int, minimo=0) -> list[dict]:
    return filtrar_por(d, "precio", lambda x: (x < maximo and x > minimo))

def mostrar_vendidos(d: list[dict], hoy=True): 
    vendidos: list[dict] = cuales_matchean(d, "disponible", False)
    if hoy:
        vendidos = cuales_matchean(vendidos, "ultimo_cambio", fecha)
        print("Estos productos se vendieron HOY")
    else:
        print("Estos son todos los productos que se vendieron")
    print_info(vendidos, "- ")

def mostrar_nuevos(d: list[dict]) -> None:
    nuevos: list[dict] = cuales_matchean(d, "fecha_agregado", fecha)
    print( "Estos productos fueron publicados HOY")
    print_info(nuevos, "+ ")

def mostrar_cambiaron_precio(d:list[dict], hoy=True) -> None:
    cambian_precio: list[dict] = filtrar_por(d, "precios_anteriores", lambda x: x != [])
    print_info(cambian_precio, "~ ")

def filtrar_de_reparacion(d: list[dict]) -> list[dict]:
    res: list[dict] = []
    for i in d:
        titulo = i["titulo"]
        if re.findall(r'\bleer\b|(no|sin) funcionar?|desbloqueo|reparar|repuestos?|colecci[óo]n|por partes', titulo, re.IGNORECASE):
            continue
        res.append(i)
    return res

# filtrado de palabras con regex
def regex_procesador(p: str) -> str:
    res: str = ""
    r_coreI = r"\b(I\d|RYZEN \d( PRO)?|R\d|CORE 2( DUO)?|CELERON|XEON|CENTRINO( DUO)?)"
    proc = re.sub(r'[^a-zA-Z0-9 -]', '', p)
    if re.findall(r_coreI, proc, re.IGNORECASE):
        res = re.search(r_coreI, proc, re.IGNORECASE).group().upper() # type: ignore
    return res

def regex_generacion(g: str) -> int:
    res = 0
    r_intel_I = r'I\d-\d{4,5}[A-Z]?\d?|\d{4,5}[A-Z]?\d?|\b\d{3}[A-Z]?'
    r_intel_full = r'I\d-\d{4,5}[A-Z]?\d?'
    r_intel_viejos = r'\b[A-Z]\d{3}\b|\bcore 2( duo)?\b|\bduo\b|\bcore 2\b|centrino( duo)?|xeon|celereon'
    r_solo_gen = r'\b\d{1,2}( ge|th|va|ma|ge|a|ta|na)|\bgen\d{1,2}'
    gen = re.sub(r'[^a-zA-Z0-9 -]', '', g)
    if re.findall(r_intel_I, gen, re.IGNORECASE):
        if re.findall(r_intel_full, gen, re.IGNORECASE):
            aux = gen.split("-")
            palabra = aux[1]
        else:
            palabra = re.search(r_intel_I, gen, re.IGNORECASE).group().upper() # type: ignore
        if int(palabra[:2]) < 14:
            res = int(palabra[:2])
        else:
            res = int(palabra[0])
    elif re.findall(r_intel_viejos, gen, re.IGNORECASE):
        palabra = re.search(r_intel_viejos, gen, re.IGNORECASE).group() # type: ignore
        res = 1
    elif re.findall(r_solo_gen, gen, re.IGNORECASE):
        palabra = re.search(r_solo_gen, gen, re.IGNORECASE).group()  # type: ignore
        res = int(re.sub(r'[^0-9]', '', palabra))
    elif re.fullmatch(r'\d{1,2}', gen):
        res = int(gen)
    elif re.findall(r'septima', gen, re.IGNORECASE):
        res = 7
    elif re.findall(r'quinto', gen, re.IGNORECASE):
        res = 5
    return res

def regex_caracteristicas(texto: str, que_buscas: str) -> str :
    '''
        Usamos un monton de regex para extraer informacion de un texto esto depende de producto, en este caso usamos notebooks 
        asi que extraemos modelo CPU, cantidad de ram y generacion dependiendo de que se especifique en que_buscas.
    '''
    que_buscas = que_buscas.upper()
    if que_buscas == "RAM" or que_buscas == "GEN":
        res: str = "0"
    else:
        res: str = ""
    rmodelo: str = r'\b(?:[A-Za-z]?\d{4}|[A-Za-z]\d{2,3}[A-Za-z]?)\b'
    rcpu: str = r'I\d'
    rram: str = r'\b\d{1,2}GB?\b'
    r_solo_gen = r'\b\d{1,2}( ge|th|va|ma|ge|a|ta)|\bgen\d{1,2}'
    r_intel_I = r'I\d-\d{4,5}[A-Z]\d?|\d{4,5}[A-Z]\d?'
    r_intel_full = r'I\d-\d{4,5}[A-Z]?\d?'
    aux = re.sub(r'[^a-zA-Z0-9 -]', '', texto)
    separado: list[str] = texto.upper().replace("-", " ").replace(",", " ").replace(".", " ").replace("\\", " ").replace("/", " ").replace("+", " ").split()
    sacar: list[str] = ["NOTEBOOK", "LAPTOP", "NETBOOK", "IMPECABLE", "OFERTA"]
    lineas: list[str] = ["LATITUDE", "LATITUD", "THINKPAD", "IDEAPAD", "ULTRABOOK", "LENOVO", "DELL"]
    if re.findall(r_intel_I, aux, re.IGNORECASE) and que_buscas == "GEN":
        if re.findall(r_intel_full, aux, re.IGNORECASE):
            aux = aux.split("-")
            palabra = aux[1]
        else:
            palabra = re.search(r_intel_I, aux, re.IGNORECASE).group().upper() # type: ignore
        if int(palabra[:2]) < 14:
            res = palabra[:2]
        else:
            res = palabra[0]
    elif re.findall(r_solo_gen, aux, re.IGNORECASE) and que_buscas == "GEN":
        palabra = re.search(r_solo_gen, aux, re.IGNORECASE).group()  # type: ignore
        res = re.sub(r'[^0-9]', '', palabra)
    for i in sacar:
        if i in separado:
            separado.remove(i)
    for i in separado:
        index = separado.index(i)
        existe_siguiente = index < len(separado) - 1
        if i in lineas and que_buscas == "LINEA":
            if i == "LENOVO":
                res = "THINKPAD"
            elif i == "DELL":
                res = "LATITUDE"
            else:
                res = i
        if re.findall(rmodelo, i) or i == "X1"and que_buscas == "MODELO":
            modelo = i.replace("(", "").replace(")", "").strip()
            if res == "":
                res = modelo
        if re.findall(rcpu, i) and que_buscas == "CPU":
            cpu = re.findall(rcpu, i)
            res = cpu[0]
        if re.findall(rram, i) and que_buscas == "RAM":
            ram = re.search(rram, i).group() # type: ignore
            numero_ram = ram.replace("G", "").replace("B", "").strip()
            res = numero_ram
        elif (re.findall(r'\b\d{1,2}\b', i) and existe_siguiente and separado[index + 1] == "GB") and que_buscas == "RAM":
            ram = i # type: ignore
            numero_ram = ram.replace("G", "").replace("B", "").strip()
            res = numero_ram
    return res
# random

def print_info(d: list[dict], puntero= "-> ") -> None:
    count = 0
    lista_productos: list[dict] = sorted(d, key=lambda x: x["precio"], reverse=True)
    for i in lista_productos:
        precio: int = i["precio"]
        producto: str = i["titulo"]
        count += 1
        print(puntero + "$" + str(precio) + ": " + producto + "\n")
    print(f"---\n{count} productos")
