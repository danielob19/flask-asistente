
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify

# Crear la app Flask
app = Flask(__name__)

# Cargar credenciales de Google desde archivo secreto
CREDENCIALES_JSON = "asistente-441318-e6835310ec59.json"  # Reemplaza con el nombre del archivo subido

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
