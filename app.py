
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde cualquier origen

@app.route('/asistente', methods=['POST'])
def asistente():
    data = request.get_json()
    if not data or 'mensaje' not in data:
        return jsonify({'error': 'Falta el campo "mensaje"'}), 400

    mensaje_usuario = data['mensaje']
    respuesta_asistente = f"Recibí tu mensaje: '{mensaje_usuario}'. Estoy procesando tu solicitud."
    return jsonify({'respuesta': respuesta_asistente})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
