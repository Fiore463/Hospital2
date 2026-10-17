# app.py - Expedientes Digitales, Hospital de Diagnóstico (Fase 2)
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# ---------------------------------------------------------------
# MARIANA SALAZAR: conexión a la base de datos
# ---------------------------------------------------------------
def conectar():
   for fila in filas:
        lista.append(fila["perfil"])
    return lista


@app.route("/")
def inicio():
    return redirect("/empleados")    conexion = sqlite3.connect("hospital.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def obtener_perfiles(conexion):
    filas = conexion.execute(
        "SELECT perfil FROM checklist GROUP BY perfil ORDER BY MIN(id)").fetchall()
    lista = []
