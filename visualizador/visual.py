from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    error = None
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        monto = request.form['monto']
        try:
            res = requests.post('http://backend:5000/convertir', json={
                'origen': origen,
                'destino': destino,
                'monto': monto
            })
            if res.status_code == 200:
                resultado = res.json()
            else:
                error = res.json().get('error', 'Error desconocido')
        except Exception as e:
            error = str(e)
    return render_template('index.html', resultado=resultado, error=error)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

