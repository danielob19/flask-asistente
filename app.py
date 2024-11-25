
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify

# Crear la app Flask
app = Flask(__name__)

# Ruta principal (opcional)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "Bienvenido al Asistente Lic. Bustamante"})

# Endpoint para manejar solicitudes
@app.route("/asistente", methods=["POST"])
def asistente():
    data = request.get_json()
    if not data or "mensaje" not in data:
        return jsonify({"error": 'Falta el campo "mensaje"'}), 400

    # Procesar el mensaje del usuario
    mensaje_usuario = data["mensaje"]
    respuesta_asistente = f"Recibí tu mensaje: '{mensaje_usuario}'. Estoy procesando tu solicitud."

    # Devuelve la respuesta al usuario
    return jsonify({"respuesta": respuesta_asistente})

# Cargar credenciales de Google desde archivo secreto
CREDENCIALES_JSON = "/etc/secrets/google_credentials.json"

def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
    client = gspread.authorize(creds)
    hoja = client.open("Asistente_Lic_Bustamante").worksheet("tab2")
    return hoja

# Verificación de funcionalidad
if __name__ == "__main__":
    try:
        hoja = conectar_google_sheets()
        print("Conexión exitosa con Google Sheets. Primera fila de datos:")
        print(hoja.row_values(1))  # Muestra la primera fila como ejemplo
    except Exception as e:
        print("Error al conectar con Google Sheets:", e)
