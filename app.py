# app.py - Expedientes Digitales, Hospital de Diagnóstico (Fase 2)
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# ---------------------------------------------------------------
# MARIANA SALAZAR: conexión a la base de datos
# ---------------------------------------------------------------
def conectar():
    conexion = sqlite3.connect("hospital.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def obtener_perfiles(conexion):
    filas = conexion.execute(
        "SELECT perfil FROM checklist GROUP BY perfil ORDER BY MIN(id)").fetchall()
    lista = []
    for fila in filas:
        lista.append(fila["perfil"])
    return lista


@app.route("/")
def inicio():
    return redirect("/empleados")




























































# FERNANDA POCASANGRE: consultar (listado con el estado del expediente)
@app.route("/empleados")
def listar():
    conexion = conectar()
    empleados = conexion.execute("SELECT * FROM empleados ORDER BY id").fetchall()
    filas_docs = conexion.execute(
        "SELECT documento FROM checklist GROUP BY documento ORDER BY MIN(id)").fetchall()
    todos = []
    for fila in filas_docs:
        todos.append(fila["documento"])

    filas = []
    for emp in empleados:
        docs = conexion.execute(
            "SELECT id, documento, estado FROM documentos WHERE empleado_id = ?",
            (emp["id"],)).fetchall()
        por_doc = {}
        for d in docs:
            por_doc[d["documento"]] = d

        celdas = []
        pendientes = 0
        for nombre_doc in todos:
            if nombre_doc in por_doc:
                d = por_doc[nombre_doc]
                if d["estado"] == "Pendiente":
                    pendientes = pendientes + 1
                celdas.append({"estado": d["estado"], "id": d["id"]})
            else:
                celdas.append({"estado": "No aplica", "id": None})

        if pendientes == 0:
            expediente = "Completo"
        else:
            expediente = "Incompleto"
        filas.append({"emp": emp, "celdas": celdas, "expediente": expediente})

    conexion.close()
    return render_template("empleados.html", filas=filas, documentos=todos)


# FERNANDA POCASANGRE: modificar el estado de un documento (con validación)
@app.route("/documentos/editar/<int:doc_id>", methods=["GET", "POST"])
def editar(doc_id):
    conexion = conectar()
    doc = conexion.execute(
        "SELECT d.id, d.documento, d.estado, e.nombre FROM documentos d "
        "JOIN empleados e ON e.id = d.empleado_id WHERE d.id = ?", (doc_id,)).fetchone()
    if doc is None:
        conexion.close()
        return redirect("/empleados")

    error = ""
    if request.method == "POST":
        estado = request.form["estado"]
        if estado != "Completo" and estado != "Pendiente":
            error = "Elige un estado: Completo o Pendiente."
        else:
            conexion.execute("UPDATE documentos SET estado = ? WHERE id = ?", (estado, doc_id))
            conexion.commit()
            conexion.close()
            return redirect("/empleados")

    conexion.close()
    return render_template("editar.html", doc=doc, error=error)
