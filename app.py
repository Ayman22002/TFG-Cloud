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
