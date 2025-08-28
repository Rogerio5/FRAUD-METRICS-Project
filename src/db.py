import sqlite3
from datetime import datetime

DB_PATH = "output/simulacoes.db"

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            data TEXT,
            custo_fp REAL,
            custo_fn REAL,
            custo_total REAL,
            vp INTEGER,
            vn INTEGER,
            fp INTEGER,
            fn INTEGER
        )
    """)
    conn.commit()
    conn.close()

def salvar_simulacao(modelo, cm, custo_fp, custo_fn):
    custo_total = cm.fp * custo_fp + cm.fn * custo_fn
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO simulacoes (modelo, data, custo_fp, custo_fn, custo_total, vp, vn, fp, fn)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        modelo,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        custo_fp,
        custo_fn,
        custo_total,
        cm.vp,
        cm.vn,
        cm.fp,
        cm.fn
    ))
    conn.commit()
    conn.close()
def consultar_simulacoes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM simulacoes ORDER BY data DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def consultar_simulacoes_filtradas(modelo=None, data=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT * FROM simulacoes WHERE 1=1"
    params = []

    if modelo:
        query += " AND modelo = ?"
        params.append(modelo)
    if data:
        query += " AND DATE(data) = ?"
        params.append(data)

    query += " ORDER BY data DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows
