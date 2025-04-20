from flask import Flask, request, jsonify
import redis
import psycopg2

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_db_conn():
    return psycopg2.connect(
        dbname='conversiones',
        user='user',
        password='pass',
        host='db'
    )

@app.route('/')
def home():
    return jsonify(msg="Conversor de Monedas en Flask está activo")

@app.route('/convertir', methods=['POST'])
def convertir():
    data = request.get_json()
    origen = data.get('origen')
    destino = data.get('destino')
    monto = float(data.get('monto', 0))

    tasa = r.get(f"{origen}_{destino}")
    if not tasa:
        return jsonify(error="Tasa de conversión no disponible aún"), 400

    tasa = float(tasa)
    resultado = monto * tasa

    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS conversiones (id SERIAL PRIMARY KEY, origen VARCHAR(3), destino VARCHAR(3), monto NUMERIC, resultado NUMERIC, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
        )
        cur.execute(
            "INSERT INTO conversiones (origen, destino, monto, resultado) VALUES (%s, %s, %s, %s)",
            (origen, destino, monto, resultado)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify(error="Error guardando en BD", detalle=str(e)), 500

    return jsonify(origen=origen, destino=destino, monto=monto, resultado=resultado, tasa=tasa)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
