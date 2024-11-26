# import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
from flask_cors import CORS  # Para habilitar CORS

# Crear la app Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde otros dominios

# Ruta principal (opcional)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "Bienvenido al Asistente Lic. Bustamante"})

# Cargar credenciales de Google desde archivo secreto
CREDENCIALES_JSON = "/etc/secrets/google_credentials.json"

def conectar_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
        client = gspread.authorize(creds)
        hoja = client.open("Asistente_Lic_Bustamante").worksheet("tab2")
        return hoja
    except Exception as e:
        print("Error al conectar con Google Sheets:", e)
        return None

# Endpoint para manejar solicitudes
@app.route("/asistente", methods=["POST"])
def asistente():
    data = request.get_json()
    if not data or "mensaje" not in data:
        return jsonify({"error": 'Falta el campo "mensaje"'}), 400

    # Procesar el mensaje del usuario
    mensaje_usuario = data["mensaje"]
    respuesta_asistente = f"Recibí tu mensaje: '{mensaje_usuario}'. Estoy procesando tu solicitud."

    # Conexión a Google Sheets
    hoja = conectar_google_sheets()
    if hoja:
        try:
            # Ejemplo: Escribir el mensaje recibido en la hoja
            hoja.append_row([mensaje_usuario, respuesta_asistente])
            respuesta_asistente += " Tu mensaje ha sido registrado en la hoja de cálculo."
        except Exception as e:
            print("Error al escribir en Google Sheets:", e)
            respuesta_asistente += " No se pudo registrar tu mensaje en la hoja de cálculo."

    # Devuelve la respuesta al usuario
    return jsonify({"respuesta": respuesta_asistente})

# Verificación de funcionalidad
if __name__ == "__main__":
    try:
        hoja = conectar_google_sheets()
        if hoja:
            print("Conexión exitosa con Google Sheets. Primera fila de datos:")
            print(hoja.row_values(1))  # Muestra la primera fila como ejemplo
        else:
            print("No se pudo conectar con Google Sheets.")
    except Exception as e:
        print("Error al conectar con Google Sheets:", e)

    # Ejecutar la app Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
