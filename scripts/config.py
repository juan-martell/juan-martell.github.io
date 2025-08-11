from datetime import date
fecha: str = date.today().strftime("%d/%m/%Y")
nombre_archivo: str = "notebooks.json" 
nombre_articulo: str = "articulos.json"
archivo_top: str = "top.json"
paginas_articulos: list[str] = [
    'dell/latitude/usado/dell-latitude',
    'lenovo/thinkpad/usado/thinkpad'
]
headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36'
    }
lista_headers: list[dict[str, str]]= [
    {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0)'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    },
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3519.1041 Mobile Safari/537.36'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.1958'
    },
    ]
