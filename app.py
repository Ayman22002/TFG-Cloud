# app.py
from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

# Inicializar base de datos en cloud
conn = sqlite3.connect('gemelo_cloud.db', check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS datos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    componente TEXT,
    variable TEXT,
    valor REAL
)
''')
conn.commit()

@app.post("/api/recibir_datos")
async def recibir_datos(request: Request):
    payload = await request.json()
    for componente, variables in payload.items():
        for var, val in variables.items():
            cursor.execute(
                "INSERT INTO datos (componente, variable, valor) VALUES (?, ?, ?)",
                (componente, var, val)
            )
    conn.commit()
    return {"mensaje": "Datos recibidos correctamente"}


@app.get("/api/datos")
def obtener_datos():
    cursor.execute("SELECT timestamp, componente, variable, valor FROM datos ORDER BY timestamp DESC LIMIT 100")
    filas = cursor.fetchall()
    return [
        {"timestamp": f[0], "componente": f[1], "variable": f[2], "valor": f[3]}
        for f in filas
    ]