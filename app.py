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
# FIORELLA FUNES: registrar empleado (con validación) y eliminar
@app.route("/empleados/nuevo", methods=["GET", "POST"])
def nuevo():
    conexion = conectar()
    perfiles = obtener_perfiles(conexion)
    error = ""
    datos = {"nombre": "", "perfil": "", "fecha_ingreso": "", "correo": ""}

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        perfil = request.form["perfil"]
        fecha = request.form["fecha_ingreso"].strip()
        correo = request.form["correo"].strip()
        datos = {"nombre": nombre, "perfil": perfil, "fecha_ingreso": fecha, "correo": correo}

        fecha_valida = True
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            fecha_valida = False

        if nombre == "":
            error = "El nombre no puede estar vacío."
        elif perfil not in perfiles:
            error = "Elige un perfil de la lista."
        elif not fecha_valida:
            error = "La fecha debe tener el formato AAAA-MM-DD (ejemplo: 2024-05-20)."
        elif "@" not in correo or "." not in correo:
            error = "Escribe un correo válido (ejemplo: nombre@hospital.com)."
        else:
            cursor = conexion.execute(
                "INSERT INTO empleados (nombre, perfil, fecha_ingreso, correo) VALUES (?, ?, ?, ?)",
                (nombre, perfil, fecha, correo))
            emp_id = cursor.lastrowid
            requeridos = conexion.execute(
                "SELECT documento FROM checklist WHERE perfil = ?", (perfil,)).fetchall()
            for r in requeridos:
                conexion.execute(
                    "INSERT INTO documentos (empleado_id, documento, estado) VALUES (?, ?, ?)",
                    (emp_id, r["documento"], "Pendiente"))
            conexion.commit()
            conexion.close()
            return redirect("/empleados")

    conexion.close()
    return render_template("nuevo.html", error=error, perfiles=perfiles, datos=datos)


@app.route("/empleados/eliminar/<int:emp_id>", methods=["POST"])
def eliminar(emp_id):
    conexion = conectar()
    conexion.execute("DELETE FROM documentos WHERE empleado_id = ?", (emp_id,))
    conexion.execute("DELETE FROM empleados WHERE id = ?", (emp_id,))
    conexion.commit()
    conexion.close()
    return redirect("/empleados")
