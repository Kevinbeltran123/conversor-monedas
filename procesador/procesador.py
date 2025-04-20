import time
import redis
import requests

r = redis.Redis(host='redis', port=6379, decode_responses=True)

monedas = ['USD', 'EUR', 'COP', 'JPY', 'GBP']
API_URL = 'https://api.exchangerate-api.com/v4/latest/{}'

while True:
    print("Consultando tasas de cambio...")
    try:
        for moneda_base in monedas:
            response = requests.get(API_URL.format(moneda_base))
            if response.status_code == 200:
                data = response.json()
                tasas = data.get('rates', {})
                for destino in monedas:
                    if destino != moneda_base and destino in tasas:
                        clave = f"{moneda_base}_{destino}"
                        valor = tasas[destino]
                        r.set(clave, valor)
                        print(f"Tasa actualizada: {clave} = {valor}")
            else:
                print(f"Error obteniendo datos para {moneda_base}")
    except Exception as e:
        print("Error en el procesador:", e)

    time.sleep(60)
